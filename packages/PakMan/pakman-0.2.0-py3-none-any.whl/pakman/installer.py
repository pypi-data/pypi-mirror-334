import subprocess
import sys
import importlib.util

def isInstalled(package: str) -> bool:
    """
    Checks if a package is installed.
    """
    return importlib.util.find_spec(package) is not None

def install(package: str, verbose: bool = False):
    """
    Installs/Upgrades the package if it's not installed.
    """
    if isInstalled(package):
        if verbose:
            print(f"{package} is already installed!")
        return

    args = [sys.executable, "-m", "pip", "install", "--upgrade", package]
    if verbose:
        print(f"Installing/Upgrading {package}...")
        subprocess.run(args, check=True)
    else:
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def runInstaller(packages: list, verbose: bool = False):
    """
    Iterates through the list of packages and installs them if they're not installed.
    """
    for package in packages:
        install(package, verbose)
