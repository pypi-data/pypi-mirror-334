#!/usr/bin/env python
"""Setup script for aws-cdk-bin package."""

import os
import sys
import platform
import subprocess
import urllib.request
import tempfile
import zipfile
import tarfile
import shutil
import json
import datetime
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

# Constants
NODE_VERSION = "18.16.0"  # LTS version
CDK_PACKAGE_NAME = "aws-cdk"
NODE_BINARIES_DIR = os.path.join("aws_cdk_bin", "node_binaries")

# Platform detection
SYSTEM = platform.system().lower()
MACHINE = platform.machine().lower()

# Map system and machine to Node.js download URLs
NODE_URLS = {
    "darwin": {
        "x86_64": f"https://nodejs.org/dist/v{NODE_VERSION}/node-v{NODE_VERSION}-darwin-x64.tar.gz",
        "arm64": f"https://nodejs.org/dist/v{NODE_VERSION}/node-v{NODE_VERSION}-darwin-arm64.tar.gz",
    },
    "linux": {
        "x86_64": f"https://nodejs.org/dist/v{NODE_VERSION}/node-v{NODE_VERSION}-linux-x64.tar.gz",
        "aarch64": f"https://nodejs.org/dist/v{NODE_VERSION}/node-v{NODE_VERSION}-linux-arm64.tar.gz",
    },
    "windows": {
        "x86_64": f"https://nodejs.org/dist/v{NODE_VERSION}/node-v{NODE_VERSION}-win-x64.zip",
    }
}

# Normalize machine architecture
if MACHINE in ("amd64", "x86_64"):
    MACHINE = "x86_64"
elif MACHINE in ("arm64", "aarch64"):
    MACHINE = "aarch64" if SYSTEM == "linux" else "arm64"

# Read the long description from README.md
def read_long_description():
    """Read the long description from README.md."""
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

def download_cdk():
    """Download and bundle the AWS CDK code."""
    node_modules_dir = os.path.join("aws_cdk_bin", "node_modules")
    
    # Clean up any existing installations
    if os.path.exists(node_modules_dir):
        print("Cleaning up existing node_modules directory")
        shutil.rmtree(node_modules_dir)
    
    os.makedirs(node_modules_dir, exist_ok=True)
    
    # Get the version to use
    version = os.environ.get("CDK_VERSION")
    
    if not version:
        print("ERROR: CDK_VERSION environment variable not set")
        raise ValueError("CDK_VERSION environment variable must be set")
    
    print(f"Downloading AWS CDK version {version}")
    
    try:
        # First try using npm if available
        try:
            # Download CDK using npm with specific version
            print(f"Running: npm pack {CDK_PACKAGE_NAME}@{version}")
            result = subprocess.run(
                ["npm", "pack", f"{CDK_PACKAGE_NAME}@{version}"], 
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Get the name of the packed file from the output
            tar_file = result.stdout.strip()
            print(f"npm pack stdout: '{tar_file}'")
            
            if not tar_file:
                # Fall back to expected filename pattern
                tar_file = f"{CDK_PACKAGE_NAME}-{version}.tgz"
                print(f"No output from npm pack, using fallback filename: {tar_file}")
                
            # Check if the file was created
            if not os.path.exists(tar_file):
                raise FileNotFoundError(f"npm pack did not create {tar_file}")
                
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            # If npm fails, download directly from npm registry
            print(f"npm command failed: {e}")
            print("Falling back to direct download from npm registry...")
            tar_file = f"{CDK_PACKAGE_NAME}-{version}.tgz"
            registry_url = f"https://registry.npmjs.org/{CDK_PACKAGE_NAME}/-/{CDK_PACKAGE_NAME}-{version}.tgz"
            
            print(f"Downloading from URL: {registry_url}")
            # Download the tarball
            import requests
            with requests.get(registry_url) as response:
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to download AWS CDK: HTTP {response.status_code}")
                    
                with open(tar_file, 'wb') as out_file:
                    out_file.write(response.content)
                    
            print(f"Successfully downloaded {tar_file}")
        
        # Extract the package
        print(f"Extracting {tar_file}")
        with tarfile.open(tar_file, 'r:gz') as tar_ref:
            # Extract to a temporary directory first
            temp_dir = tempfile.mkdtemp()
            print(f"Extracting to temporary directory: {temp_dir}")
            
            # The filter parameter was added in Python 3.12
            if sys.version_info >= (3, 12):
                tar_ref.extractall(temp_dir, filter='data')
            else:
                # For older Python versions, just use regular extractall
                tar_ref.extractall(temp_dir)
            
            # Move the files to the right place
            package_dir = os.path.join(temp_dir, "package")
            cdk_dir = os.path.join(node_modules_dir, CDK_PACKAGE_NAME)
            print(f"Moving files to: {cdk_dir}")
            
            if os.path.exists(package_dir):
                os.makedirs(cdk_dir, exist_ok=True)
                for item in os.listdir(package_dir):
                    src = os.path.join(package_dir, item)
                    dst = os.path.join(cdk_dir, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
            else:
                # No package directory, move everything
                os.makedirs(cdk_dir, exist_ok=True)
                for item in os.listdir(temp_dir):
                    src = os.path.join(temp_dir, item)
                    dst = os.path.join(cdk_dir, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
            
            # Cleanup
            print(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir)
        
        # Cleanup
        if os.path.exists(tar_file):
            print(f"Removing tarball: {tar_file}")
            os.remove(tar_file)
        
        # Create a metadata file for tracking the installed version
        metadata_path = os.path.join(node_modules_dir, CDK_PACKAGE_NAME, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump({
                "cdk_version": version,
                "installation_date": datetime.datetime.now().isoformat(),
                "build_method": "setup.py download_cdk"
            }, f, indent=2)
            
        print(f"AWS CDK version {version} successfully downloaded and installed")
        
        # Verify the installed version
        package_json_path = os.path.join(node_modules_dir, CDK_PACKAGE_NAME, "package.json")
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                installed_version = package_data.get("version")
                print(f"Verified installed CDK version: {installed_version}")
                
                if installed_version != version:
                    print(f"WARNING: Installed version {installed_version} doesn't match requested version {version}")
                    
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to download and bundle AWS CDK: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_version_file(version):
    """Update version.py with the current version."""
    version_file = os.path.join("aws_cdk_bin", "version.py")
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Use regex to replace version strings
        import re
        # Update the __version__ variable
        content = re.sub(
            r'__version__ = "[^"]+"',
            f'__version__ = "{version}"',
            content
        )
        # Update the __cdk_version__ variable
        content = re.sub(
            r'__cdk_version__ = (?:__version__|"[^"]+")',
            f'__cdk_version__ = "{version}"',
            content
        )

        with open(version_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated version.py with version {version}")

def create_readme_for_node_binaries():
    """Create a README.txt file in the node_binaries directory."""
    node_binaries_dir = os.path.join("aws_cdk_bin", "node_binaries")
    os.makedirs(node_binaries_dir, exist_ok=True)
    
    readme_path = os.path.join(node_binaries_dir, "README.txt")
    with open(readme_path, "w") as f:
        f.write("Node.js binaries will be downloaded during package installation\n")
        f.write("for the specific platform.\n")
        f.write("This approach reduces package size and ensures compatibility.\n")

class CustomBuildPy(build_py):
    """Custom build command to download CDK during build."""
    def run(self):
        # Get the target CDK version
        target_cdk_version = os.environ.get("CDK_VERSION")
        print(f"Building with CDK version: {target_cdk_version}")
        
        # Check if we need to download CDK
        cdk_dir = os.path.join("aws_cdk_bin", "node_modules", "aws-cdk")
        needs_download = True
        
        if os.path.exists(cdk_dir):
            # Check if the installed version matches the target version
            try:
                package_json_path = os.path.join(cdk_dir, "package.json")
                if os.path.exists(package_json_path):
                    with open(package_json_path, 'r') as f:
                        package_data = json.load(f)
                        installed_version = package_data.get("version")
                        print(f"Found existing CDK version: {installed_version}")
                        
                        if installed_version == target_cdk_version:
                            print("Existing CDK version matches target version, skipping download")
                            needs_download = False
                        else:
                            print(f"Existing CDK version {installed_version} doesn't match target {target_cdk_version}")
                            print("Removing existing CDK installation")
                            shutil.rmtree(cdk_dir)
            except Exception as e:
                print(f"Error checking CDK version: {e}")
                print("Will download fresh copy")
                if os.path.exists(cdk_dir):
                    shutil.rmtree(cdk_dir)
        
        # Download CDK if needed
        if needs_download:
            try:
                print(f"Downloading AWS CDK version {target_cdk_version}...")
                download_cdk()
                print("CDK download completed")
                
                # Verify the downloaded version
                package_json_path = os.path.join(cdk_dir, "package.json")
                if os.path.exists(package_json_path):
                    with open(package_json_path, 'r') as f:
                        package_data = json.load(f)
                        downloaded_version = package_data.get("version")
                        print(f"Verified downloaded CDK version: {downloaded_version}")
                        
                        if downloaded_version != target_cdk_version:
                            print(f"WARNING: Downloaded version {downloaded_version} doesn't match target {target_cdk_version}")
                
            except Exception as e:
                print(f"WARNING: Failed to download AWS CDK: {e}")
                print("Package will be built without bundled CDK, it will be downloaded at installation time.")
        
        # Create empty node_binaries directory structure
        # No need to download platform-specific binaries during build
        # They will be downloaded during post-install
        node_binaries_dir = os.path.join("aws_cdk_bin", "node_binaries")
        os.makedirs(node_binaries_dir, exist_ok=True)
        
        # Create README.txt in node_binaries directory
        create_readme_for_node_binaries()
                
        build_py.run(self)

# Custom sdist command to exclude node_modules from source distribution
class CustomSdist(sdist):
    """Custom sdist command for source distribution."""
    def make_release_tree(self, base_dir, files):
        # Call the original method
        sdist.make_release_tree(self, base_dir, files)
        
        # Remove node_modules directory from the release tree
        node_modules_dir = os.path.join(base_dir, "aws_cdk_bin", "node_modules")
        if os.path.exists(node_modules_dir):
            print(f"Removing {node_modules_dir} from source distribution")
            shutil.rmtree(node_modules_dir)
            # Create empty node_modules directory to maintain structure
            os.makedirs(node_modules_dir, exist_ok=True)
            
        # Remove node_binaries directory from the release tree
        node_binaries_dir = os.path.join(base_dir, "aws_cdk_bin", "node_binaries")
        if os.path.exists(node_binaries_dir):
            print(f"Removing {node_binaries_dir} from source distribution")
            shutil.rmtree(node_binaries_dir)
            # Create empty node_binaries directory structure
            os.makedirs(node_binaries_dir, exist_ok=True)
            
            # Add a README.txt to explain how the nodes are handled
            readme_path = os.path.join(node_binaries_dir, "README.txt")
            with open(readme_path, "w") as f:
                f.write("Node.js binaries will be downloaded during package installation\n")
                f.write("for the specific platform.\n")
                f.write("This approach reduces package size and ensures compatibility.\n")

# Custom install command that runs post-install script
class PostInstallCommand(install):
    """Post-installation steps for install mode."""
    def run(self):
        install.run(self)
        self.execute(self._post_install, [], msg="Running post-installation script...")
    
    def _post_install(self):
        # Instead of importing aws_cdk directly, run the post_install script directly
        # This avoids the chicken-and-egg problem during installation
        post_install_script = os.path.join(self.install_lib, "aws_cdk_bin", "post_install.py")
        if os.path.exists(post_install_script):
            # Make the script executable
            os.chmod(post_install_script, 0o755)
            # Run the script with the current Python interpreter
            subprocess.check_call([sys.executable, post_install_script])
        else:
            print(f"Warning: Post-installation script not found at {post_install_script}")

# Custom develop command that runs post-install script
class PostDevelopCommand(develop):
    """Post-installation steps for develop mode."""
    def run(self):
        develop.run(self)
        self.execute(self._post_install, [], msg="Running post-installation script...")
    
    def _post_install(self):
        # Run the post_install script directly
        try:
            import aws_cdk_bin.post_install
            aws_cdk_bin.post_install.main()
        except ImportError as e:
            print(f"Warning: Failed to import post_install module: {e}")
            post_install_script = os.path.join("aws_cdk_bin", "post_install.py")
            if os.path.exists(post_install_script):
                # Make the script executable
                os.chmod(post_install_script, 0o755)
                # Run the script with the current Python interpreter
                subprocess.check_call([sys.executable, post_install_script])
            else:
                print(f"Warning: Post-installation script not found at {post_install_script}")

# This setup function is used in legacy mode, but the main configuration is in pyproject.toml
if __name__ == "__main__":
    setup(
        name="aws-cdk-bin",
        version=os.environ["CDK_VERSION"],
        description="Python wrapper for AWS CDK CLI with bundled Node.js runtime",
        long_description=read_long_description(),
        long_description_content_type="text/markdown",

        url="https://github.com/rvben/aws-cdk-bin",
        packages=find_packages(),
        package_data={
            'aws_cdk_bin': [
                'node_modules/**/*', 
                'licenses/**/*',
                # Include empty node_binaries directory structure
                'node_binaries/.gitkeep',
                'node_binaries/README.txt',
            ],
        },
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'cdk=aws_cdk_bin.cli:main',
            ],
        },
        install_requires=[
            'setuptools',
            'requests',  # For downloading Node.js binaries
            'tqdm',      # For download progress bars
            'importlib_resources; python_version < "3.9"',  # For resource management
        ],
        python_requires='>=3.7',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],
        cmdclass={
            'build_py': CustomBuildPy,
            'install': PostInstallCommand,
            'develop': PostDevelopCommand,
            'sdist': CustomSdist,
        },
    )
else:
    # When imported (rather than executed), expose the custom classes for pyproject.toml
    __all__ = ['CustomBuildPy', 'PostInstallCommand', 'PostDevelopCommand', 'CustomSdist'] 