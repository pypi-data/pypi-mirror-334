from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
from pathlib import Path

class CustomInstallCommand(install):
    """Custom installation to execute all EXE files after installing and add bin/ to PATH."""
    def run(self):
        install.run(self)  # Run default install steps
        
        # Find the path to the installed package
        install_path = Path(self.install_lib) / "cadetsho" / "bin"

        # ✅ Add bin/ to system PATH
        if install_path.exists():
            bin_path = str(install_path.resolve())
            if bin_path not in os.environ["PATH"]:
                os.environ["PATH"] += os.pathsep + bin_path
                print(f"CADET bin added to PATH: {bin_path}")

            # ✅ Execute all EXE files
            for exe in install_path.glob("*.exe"):
                print(f"Running {exe} ...")
                try:
                    subprocess.run([str(exe)], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running {exe}: {e}")

setup(
    name="cadetsho",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="CADET SHO Package with bin/ Executables",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cadetsho",
    packages=find_packages(),
    package_data={"cadetsho": ["bin/*.exe", "bin/*.dll"]},  # ✅ Include all binaries
    include_package_data=True,
    install_requires=[],  # Add dependencies if needed
    cmdclass={"install": CustomInstallCommand},  # ✅ Run EXEs & add to PATH
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)

