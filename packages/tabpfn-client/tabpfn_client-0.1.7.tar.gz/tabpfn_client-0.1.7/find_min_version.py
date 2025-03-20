import subprocess
import sys
from packaging import version
import json
import requests
from datetime import datetime, timedelta
import time

# Add version check
python_version = sys.version_info
print(f"Python version: {python_version}")
if python_version < (3, 7):
    raise RuntimeError(
        f"This script requires Python 3.7 or higher. "
        f"You are using Python {sys.version.split()[0]}"
    )

PACKAGES = [
    "scikit-learn",
    'httpx',
    'omegaconf',
    'pandas',
    'password-strength',
    'cityhash',
    'sseclient-py',
    'tqdm'
]

def get_versions(package):
    """Get all stable versions of a package from PyPI"""
    try:
        r = requests.get(f"https://pypi.org/pypi/{package}/json")
        data = r.json()
        # Change to three years
        three_years_ago = datetime.now() - timedelta(days=3*365)
        versions = []
        for v, release_data in data['releases'].items():
            # Skip non-stable versions
            if any(x in v.lower() for x in ('a', 'b', 'rc', 'dev')):
                continue
            # Skip if no release data available
            if not release_data:
                continue
            # Check release date
            upload_time = datetime.fromisoformat(release_data[0]['upload_time'].replace('Z', '+00:00'))
            if upload_time >= three_years_ago:
                versions.append(v)
        return sorted(versions, key=version.parse)
    except Exception as e:
        print(f"Error fetching versions for {package}: {e}")
        return []

def test_requirements(requirements):
    """Test if the given requirements work with our test suite"""
    try:
        # Backup original requirements file
        try:
            subprocess.run(['cp', 'requirements.txt', 'requirements.txt.bak'] if sys.platform != 'win32' else ['copy', 'requirements.txt', 'requirements.txt.bak'], check=True)
        except Exception as e:
            print(f"Warning: Could not backup requirements.txt: {e}")

        # Write temporary requirements file
        with open('requirements.txt', 'w') as f:
            # Add fixed version constraints first
            f.write("respx<=0.22.0\n")
            f.write("urllib3<=2.3.0\n")
            f.write("requests<3.0.0\n")
            # Write all packages with their versions
            for pkg in PACKAGES:
                ver = requirements.get(pkg, current_versions[pkg])  # Use current version if not being tested
                f.write(f"{pkg}=={ver}\n")
        
        # Create fresh venv and install requirements
        subprocess.run(['python', '-m', 'venv', '.test_venv'], check=True)
        pip_cmd = '.test_venv/bin/pip' if sys.platform != 'win32' else r'.test_venv\Scripts\pip'
        
        # Install pytest first
        subprocess.run([pip_cmd, 'install', 'pytest'], check=True)
        subprocess.run([pip_cmd, 'install', '-r', 'requirements.txt'], check=True)
        subprocess.run([pip_cmd, 'install', '-e', '.'], check=True)
        
        # Run tests with pytest
        python_cmd = '.test_venv/bin/python' if sys.platform != 'win32' else r'.test_venv\Scripts\python'
        pytest_cmd = '.test_venv/bin/pytest' if sys.platform != 'win32' else r'.test_venv\Scripts\pytest'
        print(f"Running tests with {pytest_cmd}...")
        
        # Add verbose output and print Python path
        subprocess.run([python_cmd, '-c', 'import sys; print(sys.executable)'], check=True)
        result = subprocess.run(
            [pytest_cmd, 'tabpfn_client/tests', '-v', '--tb=short'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Test output:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False
    finally:
        # Cleanup
        subprocess.run(['rm', '-rf', '.test_venv'] if sys.platform != 'win32' else ['rmdir', '/s', '/q', '.test_venv'])
        
        # Restore original requirements file
        try:
            subprocess.run(['mv', 'requirements.txt.bak', 'requirements.txt'] if sys.platform != 'win32' else ['move', '/y', 'requirements.txt.bak', 'requirements.txt'], check=True)
        except Exception as e:
            print(f"Warning: Could not restore requirements.txt: {e}")

def find_minimum_versions():
    working_versions = {}
    
    for package in PACKAGES:
        print(f"\nChecking {package}...")
        versions = get_versions(package)
        if not versions:
            continue
            
        current_version = version.parse(current_versions[package])
        
        # Filter versions less than current
        versions = sorted([v for v in versions if version.parse(v) < current_version], 
                        key=version.parse)
        if not versions:
            continue

        print(f"Versions: {versions}")
        
        # Binary search approach
        left = 0
        right = len(versions) - 1
        last_working = None
        
        while left <= right:
            mid = (left + right) // 2
            test_version = versions[mid]
            
            print(f"Testing {package} {test_version}...")
            test_reqs = working_versions.copy()
            test_reqs[package] = test_version
            
            if test_requirements(test_reqs):
                # Version works, try an older one
                last_working = test_version
                right = mid - 1
            else:
                # Version doesn't work, try a newer one
                left = mid + 1
        
        if last_working:
            working_versions[package] = last_working
            print(f"Found minimum working version {last_working} for {package}")
        else:
            print(f"No working version found for {package}, using current version")
            working_versions[package] = current_versions[package]
            
        time.sleep(1)  # Be nice to PyPI
    
    return working_versions

# Current versions from your requirements
current_versions = {
    'httpx': '0.27.2',
    'omegaconf': '2.3.0',
    'pandas': '2.2.3',
    'password-strength': '0.0.3.post2',
    'cityhash': '0.4.7',
    'sseclient-py': '1.8.0',
    'tqdm': '4.67.1',
    'scikit-learn': '1.6.0'
}

print("Finding minimum working versions...")
min_versions = find_minimum_versions()
