import numpy as np
import time
import hashlib
import csv
import io
import timeit
from tabpfn_client.tabpfn_common_utils import utils as common_utils

# Try to import various hash libraries
try:
    import cityhash
    has_cityhash = True
except ImportError:
    has_cityhash = False
    print("cityhash not installed, skipping cityhash benchmark")

try:
    import xxhash
    has_xxhash = True
except ImportError:
    has_xxhash = False
    print("xxhash not installed, skipping xxhash benchmark")

def generate_random_dataset(n_rows=10000, n_cols=500):
    """Generate a random dataset of specified size"""
    return np.random.random((n_rows, n_cols))

def serialize_dataset(data):
    """Serialize numpy array to CSV formatted bytes (similar to the client implementation)"""
    return common_utils.serialize_to_csv_formatted_bytes(data)

def hash_with_cityhash(data_bytes):
    """Hash using cityhash"""
    return cityhash.CityHash64(data_bytes)

def hash_with_md5(data_bytes):
    """Hash using MD5"""
    return hashlib.md5(data_bytes).hexdigest()

def hash_with_blake2b(data_bytes):
    """Hash using BLAKE2b with 16-byte digest"""
    return hashlib.blake2b(data_bytes, digest_size=16).hexdigest()

def hash_with_xxhash(data_bytes):
    """Hash using xxHash"""
    return xxhash.xxh64(data_bytes).hexdigest()

def hash_with_python(data_bytes):
    """Hash using Python's built-in hash function"""
    # Since hash() doesn't work on bytes directly in a consistent way,
    # we'll convert to a tuple of integers
    return hash(tuple(data_bytes))

def benchmark_hash_functions(data, num_runs=5):
    """Benchmark different hash functions on the given data"""
    data_bytes = serialize_dataset(data)
    
    results = {}
    
    # MD5 benchmark
    start = time.time()
    for _ in range(num_runs):
        hash_with_md5(data_bytes)
    md5_time = (time.time() - start) / num_runs
    results['MD5'] = md5_time
    
    # BLAKE2b benchmark
    start = time.time()
    for _ in range(num_runs):
        hash_with_blake2b(data_bytes)
    blake2b_time = (time.time() - start) / num_runs
    results['BLAKE2b'] = blake2b_time
    
    # Python's hash benchmark
    # Note: This might be very slow for large data
    try:
        start = time.time()
        for _ in range(num_runs):
            hash_with_python(data_bytes[:10000])  # Using only part of the data to avoid timeout
        python_hash_time = (time.time() - start) / num_runs
        # Estimate full time based on proportion
        estimated_full_time = python_hash_time * (len(data_bytes) / 10000)
        results['Python hash (est.)'] = estimated_full_time
    except Exception as e:
        print(f"Python hash failed: {e}")
    
    # xxHash benchmark (if available)
    if has_xxhash:
        start = time.time()
        for _ in range(num_runs):
            hash_with_xxhash(data_bytes)
        xxhash_time = (time.time() - start) / num_runs
        results['xxHash'] = xxhash_time
    
    # CityHash benchmark (if available)
    if has_cityhash:
        start = time.time()
        for _ in range(num_runs):
            hash_with_cityhash(data_bytes)
        cityhash_time = (time.time() - start) / num_runs
        results['CityHash'] = cityhash_time
    
    return results

def main():
    print("Generating random dataset (10,000 x 500)...")
    data = generate_random_dataset(10000, 500)
    
    print("Dataset size (MB):", data.nbytes / (1024 * 1024))
    
    print("\nSerializing dataset...")
    serialized_size = len(serialize_dataset(data))
    print("Serialized size (MB):", serialized_size / (1024 * 1024))
    
    print("\nBenchmarking hash functions (average of 5 runs)...")
    results = benchmark_hash_functions(data)
    
    # Print results in a formatted table
    print("\nResults:")
    print("-" * 60)
    print(f"{'Hash Function':<20} | {'Time (seconds)':<15} | {'Relative Speed':<15}")
    print("-" * 60)
    
    # Find fastest algorithm for relative comparison
    fastest_time = min(results.values())
    
    for func, timing in sorted(results.items(), key=lambda x: x[1]):
        relative = timing / fastest_time
        print(f"{func:<20} | {timing:.6f}s        | {relative:.2f}x")
    
    print("-" * 60)

if __name__ == "__main__":
    main()
