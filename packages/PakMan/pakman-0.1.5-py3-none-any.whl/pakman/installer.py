import subprocess
import sys
import importlib.util

class PackageInstaller:
    def __init__(self, packages):
        """
        param packages: List of package names to install.
        """
        self.packages = packages

    def install(self, package):
        """
        param package: The name of the package to install.
        """
        print(f"Installing/Upgrading {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def isInstalled(self, package):
        """
        Checks if a package is installed.
        """
        return importlib.util.find_spec(package) is not None

    def runInstaller(self):
        """
        Checks if each package is installed, and installs it if not.
        """
        for package in self.packages:
            if not self.isInstalled(package):
                self.install(package)
