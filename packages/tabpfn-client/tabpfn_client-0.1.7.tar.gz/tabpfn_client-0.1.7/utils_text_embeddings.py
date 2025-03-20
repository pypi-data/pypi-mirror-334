import asyncio
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.decomposition import PCA
from sklearn.preprocessing import TargetEncoder
import warnings


# taken from https://github.com/skrub-data/skrub/blob/main/skrub/_utils.py
def unique_strings(values, is_null):
    """Unique values, accounting for nulls.

    This is like np.unique except
    - it is only for 1d arrays of strings
    - caller must pass a boolean array indicating which values are null: ``is_null``
    - null values are considered to be the same as the empty string.

    >>> import numpy as np
    >>> import pandas as pd
    >>> from skrub._utils import unique_strings
    >>> a = np.asarray(['paris', '', 'berlin', None, 'london'])
    >>> values, idx = unique_strings(a, pd.isna(a))
    >>> values
    array(['', 'berlin', 'london', 'paris'], dtype=object)
    >>> values[idx]
    array(['paris', '', 'berlin', '', 'london'], dtype=object)
    """
    not_null_values = values[~is_null]
    unique, idx = np.unique(not_null_values, return_inverse=True)
    if not is_null.any():
        return unique, idx
    if not len(unique) or unique[0] != "":
        unique = np.concatenate([[""], unique])
        idx += 1
    full_idx = np.empty(values.shape, dtype=idx.dtype)
    full_idx[is_null] = 0
    full_idx[~is_null] = idx
    return unique, full_idx


def match_embeddings(
    texts: np.ndarray, embedding_dict: Dict[str, np.ndarray]
) -> np.ndarray:
    # Handle missing values
    is_null = pd.isna(texts)
    unique_texts, inverse_indices = unique_strings(texts, is_null)

    # Remove empty strings and get embeddings for non-empty texts
    non_empty_mask = unique_texts != ""
    non_empty_texts = unique_texts[non_empty_mask]
    unique_embeddings = np.array([embedding_dict[text] for text in non_empty_texts])

    # Create nan embeddings for missing/empty values
    embedding_dim = next(iter(embedding_dict.values())).shape[0]
    full_embeddings = np.full((len(unique_texts), embedding_dim), np.nan)
    full_embeddings[non_empty_mask] = unique_embeddings

    # Use inverse indices to reconstruct the original order and structure
    matched_embeddings = full_embeddings[inverse_indices]

    return matched_embeddings


# this should only be run after we have converted all columns to the correct type
# with skrub
def find_text_columns(df: pd.DataFrame) -> List[str]:
    return [col for col in df.columns if df[col].dtype == object]


class TextEmbedder:
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        chunk_size: int = 1000,
        dimension_openai: int = 256,
        dimension_final: int = 16,
        dim_reduction: str = "pca",
        max_features: int = 500,
        max_embedded_cols: int = 15,
    ):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.chunk_size = chunk_size
        self.dimension_openai = dimension_openai
        self.dimension_final = dimension_final
        self.max_features = max_features
        self.max_embedded_cols = max_embedded_cols
        self.dim_reduction = dim_reduction
        self.embeddings = {}
        self.text_columns = None
        self.ignored_text_columns = []
        self.dimension_reduction_transformers = {}
        self.target_encoder = None

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=5),
        stop=stop_after_attempt(3)
    )
    async def embed_chunk(self, chunk: List[str]) -> List[List[float]]:
        # Simulated API call delay
        await asyncio.sleep(0.001)
        response = await self.client.embeddings.create(
            input=chunk, model=self.model, dimensions=self.dimension_openai
        )
        return [item.embedding for item in response.data]

    async def embed_column(
        self, column: pd.Series, column_name: str, during_transform: bool = False
    ) -> None:
        values, is_null = column.values, pd.isna(column)
        unique_values, _ = unique_strings(values, is_null)

        # Remove empty strings from unique values
        unique_values = [value for value in unique_values if value != ""]
        new_values = unique_values

        # Identify new values that need to be embedded
        if column_name in self.embeddings:
            if during_transform:
                new_values = set(unique_values) - set(self.embeddings[column_name].keys())
                new_values = list(new_values)
            else:
                # During fit_transform, we embed all unique values
                self.embeddings[column_name] = {}

        if len(new_values) > 0:
            # Split new values into chunks
            chunks = [
                new_values[i : i + self.chunk_size]
                for i in range(0, len(new_values), self.chunk_size)
            ]

            # Embed chunks
            embedded_chunks = await asyncio.gather(
                *[self.embed_chunk(chunk) for chunk in chunks]
            )
            # Flatten the embedded chunks
            all_embeddings = np.vstack(
                [emb for chunk in embedded_chunks for emb in chunk]
            )

            # Apply dimensionality reduction
            if not during_transform:
                all_embeddings = self.dimension_reduction_transformers[
                    column_name
                ].fit_transform(all_embeddings)
            else:
                all_embeddings = self.dimension_reduction_transformers[
                    column_name
                ].transform(all_embeddings)

            # Map new values to their embeddings
            new_embedding_dict = dict(zip(new_values, all_embeddings))

            # Update the embeddings dictionary for this column
            if column_name not in self.embeddings:
                self.embeddings[column_name] = {}
            self.embeddings[column_name].update(new_embedding_dict)

    async def compute_dataframe_embeddings(
        self,
        df: pd.DataFrame,
        y: pd.Series = None,
        during_transform: bool = False,
    ) -> None:
        tasks = [
            self.embed_column(df[col], col, during_transform)
            for col in self.text_columns
        ]
        await asyncio.gather(*tasks)

    def compute_text_columns_and_dimensions(self, df: pd.DataFrame):
        # Limit the number of text columns to embed if necessary
        text_columns = self.text_columns[: self.max_embedded_cols]
        ignored_text_columns = self.text_columns[self.max_embedded_cols :]

        # Calculate number of non-text columns that will remain
        non_text_features = len(df.columns) - len(text_columns)

        # Calculate remaining features available for embeddings
        remaining_features = max(0, self.max_features - non_text_features)

        # Ensure the total number of features after embedding does not exceed max_features
        MIN_DIMENSIONS = 1
        if len(text_columns) > 0:
            dimension_final = max(
                MIN_DIMENSIONS,
                min(self.dimension_final, remaining_features // len(text_columns)),
            )
        else:
            dimension_final = self.dimension_final

        # If the dataframe is too small, we don't need to embed any columns
        if len(df) <= dimension_final:
            ignored_text_columns = self.text_columns
            text_columns = []

        return text_columns, ignored_text_columns, dimension_final

    async def fit_transform(self, X: pd.DataFrame, y: pd.Series = None) -> pd.DataFrame:
        self.text_columns = find_text_columns(X)
        if not self.text_columns:
            return X.copy()
        self.ignored_text_columns = []

        try:
            (
                self.text_columns,
                self.ignored_text_columns,
                self.dimension_final,
            ) = self.compute_text_columns_and_dimensions(X)

            # Set up dimension reduction
            for col in self.text_columns:
                if self.dim_reduction == "pca":
                    pca = PCA(n_components=self.dimension_final)
                    self.dimension_reduction_transformers[col] = pca
                else:
                    raise ValueError(
                        f"Unsupported dimension reduction method: {self.dim_reduction}"
                    )

            # Asynchronously compute embeddings
            await self.compute_dataframe_embeddings(X, y)

        except Exception:
            warnings.warn(
                """Couldn't handle text columns properly. Falling back to a simple method, performance will be worse.
                          Try again in a few minutes if the issue persists.""",
                UserWarning,
            )
            self.ignored_text_columns = self.text_columns
            self.text_columns = []

        # Use fit_transform of TargetEncoder and replace the columns in X
        X_transformed = X.copy()
        if len(self.ignored_text_columns) > 0:
            self.target_encoder = TargetEncoder(target_type="continuous", random_state=34)
            X_encoded = self.target_encoder.fit_transform(
                X[self.ignored_text_columns], y
            )
            # Replace the original columns with the transformed ones
            X_transformed.loc[:, self.ignored_text_columns] = X_encoded

        # Apply embeddings to the dataframe
        X_transformed = self._apply_embeddings(X_transformed)

        return X_transformed

    async def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.text_columns and not self.ignored_text_columns:
            return X.copy()

        X_transformed = X.copy()

        if len(self.ignored_text_columns) > 0 and self.target_encoder is not None:
            X_encoded = self.target_encoder.transform(
                X[self.ignored_text_columns]
            )
            # Replace the original columns with the transformed ones
            X_transformed.loc[:, self.ignored_text_columns] = X_encoded

        await self._transform(X_transformed)

        # Apply embeddings to the dataframe
        X_transformed = self._apply_embeddings(X_transformed)

        return X_transformed

    async def _transform(self, X: pd.DataFrame):
        await self.compute_dataframe_embeddings(X, during_transform=True)

    def _apply_embeddings(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.text_columns:
            return X

        new_columns = {}
        for col in self.text_columns:
            # Get embeddings for this column
            col_embeddings = match_embeddings(X[col].values, self.embeddings[col])

            for i in range(col_embeddings.shape[1]):
                new_columns[f"{col}_emb_{i}"] = col_embeddings[:, i]

        embedded_df = pd.DataFrame(new_columns, index=X.index)
        X_transformed = pd.concat(
            [X.drop(columns=self.text_columns), embedded_df], axis=1
        )
        return X_transformed


class PredictorWithTextEmbeddings:
    """A scikit-learn compatible transformer that enriches data with text embeddings"""

    def __init__(
        self,
        base_predictor,
        api_key: str = None,
    ):
        self.base_predictor = base_predictor
        # check is api_key is in the environment variables
        if api_key is None:
            openai_api_key = "test_api_key"
        else:
            openai_api_key = api_key
        self.text_embedder = TextEmbedder(
            api_key=openai_api_key,
        )

    def save_state(self):
        pass

    def load_state(self):
        pass

    async def fit(
        self,
        x_train: pd.DataFrame,
        y_train: pd.DataFrame,
    ):
        """Fits the base predictor on the enriched data"""
        x_train_copy = x_train.copy()
        y_train_copy = y_train.copy()
        x_train_enriched = await self.text_embedder.fit_transform(x_train_copy, y_train_copy)

        self.save_state()
        self.base_predictor.fit(
            x_train_enriched,
            y_train_copy,
        )

    async def _before_predict(
        self,
        x_test: pd.DataFrame,
    ):
        self.load_state()
        x_test_copy = x_test.copy()
        await self.text_embedder.compute_dataframe_embeddings(
            x_test_copy, during_transform=True
        )
        x_test_enriched = await self.text_embedder.transform(x_test_copy)
        return x_test_enriched

    async def predict(
        self,
        x_test: pd.DataFrame,
    ):
        # Make predictions using enriched features
        x_test_enriched = await self._before_predict(x_test)
        return  self.base_predictor.predict(x_test_enriched)

    async def predict_proba(
        self,
        x_test: pd.DataFrame,
    ):
        x_test_enriched = await self._before_predict(x_test)
        return self.base_predictor.predict_proba(x_test_enriched)


import numpy as np
import pandas as pd
from skrub import TableVectorizer
from sklearn.preprocessing import OrdinalEncoder


class PredictorWithSkrub:
    """A scikit-learn compatible transformer that preprocesses data before fitting a predictor"""

    def __init__(
        self,
        base_predictor,
    ):
        self.base_predictor = base_predictor
        self.table_vectorizer = TableVectorizer(
            low_cardinality=OrdinalEncoder(
                handle_unknown="use_encoded_value", unknown_value=np.nan
            ),
            high_cardinality="passthrough",
            cardinality_threshold=30,
            numeric="passthrough",
        )

    def save_state(self):
        pass

    def load_state(self):
        pass

    async def fit(
        self,
        x_train,
        y_train,
    ):
        x_train_transformed = self.table_vectorizer.fit_transform(x_train)
        self.save_state()
        return await self.base_predictor.fit(
            x_train_transformed,
            y_train,
        )

    async def _before_predict(
        self,
        x_test: pd.DataFrame,
    ):
        self.load_state()
        x_test_transformed = self.table_vectorizer.transform(x_test)
        return x_test_transformed

    async def predict(
        self,
        x_test: pd.DataFrame,
    ):
        x_test_transformed = await self._before_predict(x_test)

        # Make predictions using transformed features
        return await self.base_predictor.predict(x_test_transformed)

    async def predict_proba(
        self,
        x_test: pd.DataFrame,
    ):
        x_test_transformed = await self._before_predict(x_test)
        return await self.base_predictor.predict_proba(x_test_transformed)


from sklearn.model_selection import BaseCrossValidator
from sklearn.utils import indexable
from sklearn.utils.validation import _num_samples
import numpy as np

class FixedSizeSplit(BaseCrossValidator):
    def __init__(self, n_train: int, n_test: int = None, n_splits: int = 5, random_state: int = None,
                 keep_pandas=False) -> None:
        self.n_train = n_train
        self.n_test = n_test
        self.n_splits = n_splits
        self.random_state = random_state
        self.keep_pandas = keep_pandas

    def get_n_splits(self, X=None, y=None, groups=None) -> int:
        return self.n_splits

    def split(self, X, y=None, groups=None):
        X, y, groups = indexable(X, y, groups)
        n_samples = _num_samples(X)

        if self.n_train > n_samples:
            raise ValueError(f"Cannot set n_train={self.n_train} greater than the number of samples: {n_samples}.")

        if self.n_test is not None and self.n_test > n_samples - self.n_train:
            raise ValueError(f"Cannot set n_test={self.n_test} greater than the remaining samples: {n_samples - self.n_train}.")

        indices = np.arange(n_samples)

        rng = np.random.default_rng(self.random_state)

        for i in range(self.n_splits):
            indices_copy = indices.copy()
            rng.shuffle(indices_copy)
            
            train = indices_copy[:self.n_train]
            
            if self.n_test is not None:
                test = indices_copy[self.n_train:self.n_train + self.n_test]
            else:
                test = indices_copy[self.n_train:]
            
            yield train, test
