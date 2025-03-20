import subprocess
import sys
import re
from typing import List, Tuple

def run_command(command: List[str]) -> Tuple[str, str, int]:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

def install_package(package: str) -> bool:
    print(f"Installing {package}...")
    _, _, code = run_command([sys.executable, "-m", "pip", "install", package])
    return code == 0

def run_tests() -> Tuple[bool, str]:
    _, stderr, code = run_command([
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tabpfn_client/tests",
        "-t",
        "tabpfn_client/tests"
    ])
    has_respx_error = "respx.models.AllMockedAssertionError" in stderr
    return not has_respx_error, stderr

def main():
    # Save original package versions
    packages_to_test = [
        ("httpx", ["0.27.2", "0.28.1"]),
        ("httpcore", ["1.0.6", "1.0.7"]),
        ("anyio", ["4.6.2.post1", "4.7.0"]),
        ("attrs", [None, "latest"]),
        ("charset-normalizer", [None, "latest"]),
        ("safehttpx", [None, "latest"])
    ]
    
    original_versions = {}
    for package, _ in packages_to_test:
        result = run_command([sys.executable, "-m", "pip", "show", package])
        if result[0]:  # if package is installed
            version = re.search(r"Version: (.+)", result[0])
            if version:
                original_versions[package] = version.group(1)
        else:
            original_versions[package] = None

    print("Original versions:", original_versions)

    # Test each package combination
    for i, (package, versions) in enumerate(packages_to_test):
        for version in versions:
            if version is None:
                run_command([sys.executable, "-m", "pip", "uninstall", "-y", package])
            else:
                package_spec = f"{package}=={version}" if version != "latest" else package
                install_package(package_spec)
            
            success, error_output = run_tests()
            current_versions = {pkg: run_command([sys.executable, "-m", "pip", "show", pkg])[0].split("Version: ")[1].split("\n")[0] 
                              if run_command([sys.executable, "-m", "pip", "show", pkg])[0] else None 
                              for pkg, _ in packages_to_test}
            
            print(f"\nTest with {package} {'uninstalled' if version is None else f'version {version}'}:")
            print(f"Current versions: {current_versions}")
            print(f"Test {'passed' if success else 'failed'}")
            
            if success:
                print("\nFound working configuration!")
                print("Required changes from original:")
                for pkg, curr_ver in current_versions.items():
                    orig_ver = original_versions.get(pkg)
                    if curr_ver != orig_ver:
                        print(f"{pkg}: {orig_ver} -> {curr_ver}")
                
                # Provide pip commands to make these changes
                print("\nCommands to apply these changes:")
                for pkg, curr_ver in current_versions.items():
                    orig_ver = original_versions.get(pkg)
                    if curr_ver != orig_ver:
                        if curr_ver is None:
                            print(f"pip uninstall -y {pkg}")
                        else:
                            print(f"pip install {pkg}=={curr_ver}")
                
                return

    print("\nNo working configuration found.")

if __name__ == "__main__":
    main()
