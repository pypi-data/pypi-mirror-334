import subprocess
import sys
import importlib.util

class PackageInstaller:
    def __init__(self, packages):
        """
        param packages: List of package names to install.
        """
        self.packages = packages

    def install(self, package, verbose=False):
        print(f"Installing/Upgrading {package}...")
        args = [sys.executable, "-m", "pip", "install", "--upgrade", package]
        if verbose:
            subprocess.run(args)
        else:
            subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def isInstalled(self, package):
        """
        Checks if a package is installed.
        """
        return importlib.util.find_spec(package) is not None

    def runInstaller(self, verbose=False):
        """
        Checks if each package is installed, and installs it if not.
        """
        for package in self.packages:
            if not self.isInstalled(package):
                self.install(package, verbose)
