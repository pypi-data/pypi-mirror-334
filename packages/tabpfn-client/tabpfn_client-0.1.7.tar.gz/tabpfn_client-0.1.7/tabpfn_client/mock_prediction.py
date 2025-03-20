import threading
import contextlib
from typing import Literal
import numpy as np
import time
from unittest import mock
import warnings
import logging
import functools

from tabpfn_client.client import ServiceClient
from tabpfn_client.tabpfn_common_utils.expense_estimation import estimate_duration


COST_ESTIMATION_LATENCY_OFFSET = 1.0


# For seamlessly switching between a mock mode for simulating prediction
# costs and real prediction, use thread-local variables to keep track of the
# current mode, simulated costs and time.
_thread_local = threading.local()


# Block of small helper functions to access and modify the thread-local
# variables used for mock prediction in a simple and unified way.
def is_mock_mode() -> bool:
    return getattr(_thread_local, "use_mock", False)


def set_mock_mode(value: bool):
    setattr(_thread_local, "use_mock", value)


def get_mock_cost() -> float:
    return getattr(_thread_local, "cost", 0.0)


def increment_mock_cost(value: float):
    setattr(_thread_local, "cost", get_mock_cost() + value)


def set_mock_cost(value: float = 0.0):
    setattr(_thread_local, "cost", value)


def get_mock_time() -> float:
    return getattr(_thread_local, "mock_time")


def set_mock_time(value: float):
    setattr(_thread_local, "mock_time", value)


def increment_mock_time(seconds: float):
    set_mock_time(get_mock_time() + seconds)


def mock_predict(
    X_test,
    task: Literal["classification", "regression"],
    train_set_uid: str,
    X_train,
    y_train,
    config=None,
    predict_params=None,
):
    """
    Mock function for prediction, which can be called instead of the real
    prediction function. Outputs random results in the expacted format and
    keeps track of the simulated cost and time.
    """
    if X_train is None or y_train is None:
        raise ValueError(
            "X_train and y_train must be provided in mock mode during prediction."
        )

    duration = estimate_duration(
        num_rows=X_train.shape[0] + X_test.shape[0],
        num_features=X_test.shape[1],
        task=task,
        tabpfn_config=config,
        latency_offset=COST_ESTIMATION_LATENCY_OFFSET,  # To slightly overestimate (safer)
    )
    increment_mock_time(duration)

    cost = (
        (X_train.shape[0] + X_test.shape[0])
        * X_test.shape[1]
        * config.get("n_estimators", 4 if task == "classification" else 8)
    )
    increment_mock_cost(cost)

    # Return random result in the correct format
    if task == "classification":
        if (
            not predict_params["output_type"]
            or predict_params["output_type"] == "preds"
        ):
            return np.random.rand(X_test.shape[0])
        elif predict_params["output_type"] == "probas":
            probs = np.random.rand(X_test.shape[0], len(np.unique(y_train)))
            return probs / probs.sum(axis=1, keepdims=True)

    elif task == "regression":
        if not predict_params["output_type"] or predict_params["output_type"] == "mean":
            return np.random.rand(X_test.shape[0])
        elif predict_params["output_type"] == "full":
            return {
                "logits": np.random.rand(X_test.shape[0], 5000),
                "mean": np.random.rand(X_test.shape[0]),
                "median": np.random.rand(X_test.shape[0]),
                "mode": np.random.rand(X_test.shape[0]),
                "quantiles": np.random.rand(3, X_test.shape[0]),
                "borders": np.random.rand(5001),
                "ei": np.random.rand(X_test.shape[0]),
                "pi": np.random.rand(X_test.shape[0]),
            }


@contextlib.contextmanager
def mock_mode():
    """
    Context manager that enables mock mode in the current thread.
    """
    old_value = is_mock_mode()
    set_mock_mode(True)
    set_mock_cost(0.0)
    set_mock_time(time.time())

    # Store original logging levels for all loggers
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    loggers.append(logging.getLogger())  # Add root logger
    original_levels = {logger: logger.level for logger in loggers}

    # Suppress all warnings and logging
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Set all loggers to ERROR level
        for logger in loggers:
            logger.setLevel(logging.ERROR)

        with mock.patch("time.time", side_effect=get_mock_time):
            try:
                yield lambda: get_mock_cost()
            finally:
                set_mock_mode(old_value)
                # Restore original logging levels
                for logger in loggers:
                    logger.setLevel(original_levels[logger])


def check_api_credits(func):
    """
    Decorator that first runs the decorated function in mock mode to simulate its credit usage.
    If user has enough credits, function is then executed for real.
    """
    from tabpfn_client import get_access_token

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with mock_mode() as get_mock_cost:
            func(*args, **kwargs)
            credit_estimate = get_mock_cost()
        access_token = get_access_token()
        api_usage = ServiceClient.get_api_usage(access_token)

        if (
            not api_usage["usage_limit"] == -1
            and api_usage["usage_limit"] - api_usage["current_usage"] < credit_estimate
        ):
            raise RuntimeError(
                f"Not enough credits left. Estimated credit usage: {credit_estimate}, credits left: {api_usage['usage_limit'] - api_usage['current_usage']}"
            )
        else:
            print("Enough credits left.")

        return func(*args, **kwargs)

    return wrapper
