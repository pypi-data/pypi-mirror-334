from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys

class CustomInstallCommand(install):
    """Custom installation to add cadetsho/bin to PATH (only for the current environment)."""
    
    def run(self):
        install.run(self)  # Run default install steps

        # Find the installed package path
        bin_path = os.path.abspath(os.path.join(self.install_lib, "cadetsho", "bin"))

        # ✅ Add bin/ to PATH (for the current session only)
        if os.path.exists(bin_path):
            print(f"Adding CADET bin to PATH (for this environment only): {bin_path}")
            os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
            print("Run `cadet-cli --version` to verify installation.")

setup(
    name="cadetsho",
    version="0.1.2",  # Increment version
    packages=find_packages(),
    package_data={"cadetsho": ["bin/*.exe", "bin/*.dll"]},  # Include binaries
    include_package_data=True,
    install_requires=[],
    cmdclass={"install": CustomInstallCommand},  # ✅ Runs post-install script
)

