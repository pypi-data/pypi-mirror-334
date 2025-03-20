import subprocess
import sys
import importlib.util

class PackageInstaller:
    @staticmethod
    def isInstalled(package: str) -> bool:
        """
        Checks if a package is installed.
        """
        return importlib.util.find_spec(package) is not None
    
    @classmethod
    def install(cls, package: str, verbose: bool = False):
        """
        Installs/Upgrades the package if it's not installed.
        """
        if not cls.isInstalled(package):
            args = [sys.executable, "-m", "pip", "install", "--upgrade", package]
            if verbose:
                print(f"Installing/Upgrading {package}...")
                subprocess.run(args, check=True)
            else:
                subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    @classmethod
    def runInstaller(cls, packages: list, verbose: bool = False):
        """
        Iterates through the list of packages and installs them if they're not installed.
        """
        for package in packages:
            if not cls.isInstalled(package):
                cls.install(package, verbose)
