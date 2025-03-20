from setuptools import setup, find_packages
import subprocess
import sys
import pkg_resources
from pathlib import Path
from typing import List, Dict, Any
import os
import platform
import shutil

def create_system_link():
    """Create system-wide executable link for qgit."""
    try:
        system = platform.system().lower()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        venv_dir = os.path.join(script_dir, ".venv")
        
        if system in ['linux', 'darwin']:  # Linux or macOS
            target_dir = '/usr/local/bin'
            if not os.access(target_dir, os.W_OK):
                print(f"Warning: No write access to {target_dir}. Using user's local bin directory.")
                target_dir = os.path.expanduser('~/.local/bin')
                os.makedirs(target_dir, exist_ok=True)
            
            target_path = os.path.join(target_dir, 'qgit')
            script_path = os.path.join(script_dir, 'qgit')
            
            # Create the executable script with venv path
            with open(script_path, 'w') as f:
                f.write(f"""#!/usr/bin/env python3
\"\"\"Main entry point for QGit commands.\"\"\"

import sys
import os
from pathlib import Path

# Add the package directory to Python path
package_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(package_dir))

# Add the virtual environment site-packages if it exists
venv_site_packages = package_dir / ".venv" / "lib" / "python3.12" / "site-packages"
if venv_site_packages.exists():
    sys.path.insert(0, str(venv_site_packages))

from qgits.qgit import main

if __name__ == "__main__":
    sys.exit(main())
""")
            os.chmod(script_path, 0o755)  # Make executable
            
            # Create symlink
            if os.path.exists(target_path):
                os.remove(target_path)
            os.symlink(script_path, target_path)
            print(f"✓ Created system link at {target_path}")
            
        elif system == 'windows':
            # Windows: Add to PATH by creating a batch file
            target_dir = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'QGit')
            os.makedirs(target_dir, exist_ok=True)
            
            batch_path = os.path.join(target_dir, 'qgit.bat')
            script_path = os.path.join(script_dir, 'qgit.py')
            
            # Create Python script
            with open(script_path, 'w') as f:
                f.write(f"""#!/usr/bin/env python3
\"\"\"Main entry point for QGit commands.\"\"\"

import sys
import os
from pathlib import Path

# Add the package directory to Python path
package_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(package_dir))

# Add the virtual environment site-packages if it exists
venv_site_packages = package_dir / ".venv" / "lib" / "python3.12" / "site-packages"
if venv_site_packages.exists():
    sys.path.insert(0, str(venv_site_packages))

from qgits.qgit import main

if __name__ == "__main__":
    sys.exit(main())
""")
            
            # Create batch file that uses local Python
            with open(batch_path, 'w') as f:
                f.write(f"""@echo off
set PYTHONPATH={script_dir}
"{os.path.join(venv_dir, 'Scripts', 'python.exe')}" "{script_path}" %*
""")
            
            # Add to PATH if not already there
            path_var = os.environ.get('PATH', '')
            if target_dir not in path_var:
                os.environ['PATH'] = f"{path_var};{target_dir}"
                # Try to update system PATH
                try:
                    subprocess.run(['setx', 'PATH', os.environ['PATH']], check=True)
                except subprocess.CalledProcessError:
                    print("Warning: Could not update system PATH. Please add manually:")
                    print(f"Add {target_dir} to your system's PATH environment variable")
            
            print(f"✓ Created Windows executable at {batch_path}")
        
        return True
    except Exception as e:
        print(f"Warning: Failed to create system link: {e}")
        return False

def verify_dependencies() -> bool:
    """Verify all required dependencies are installed and accessible."""
    required_packages = [
        "pygame>=2.5.2,<3.0.0",
        "numpy>=1.26.0,<2.0.0",
        "PyOpenGL>=3.1.7,<4.0.0",
        "PyOpenGL-accelerate>=3.1.7,<4.0.0",
        "gitpython>=3.1.40,<4.0.0",
        "psutil>=5.9.6,<6.0.0",
        "python-dotenv>=1.0.0,<2.0.0",
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            pkg_resources.require(package)
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict) as e:
            missing_packages.append(f"{package} ({str(e)})")
    
    if missing_packages:
        print("Warning: Missing or incompatible dependencies:")
        for package in missing_packages:
            print(f"  - {package}")
        return False
    return True

def ensure_env_directory():
    """Ensure the internal directory and .env file exist."""
    internal_dir = Path("internal")
    env_file = internal_dir / ".env"
    
    if not internal_dir.exists():
        internal_dir.mkdir(parents=True)
        print("✓ Created internal directory")
    
    if not env_file.exists():
        env_file.touch()
        print("✓ Created .env file")

def install_dependencies() -> bool:
    """Install missing dependencies using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def run_setup_verification():
    """Run setup verification after installation."""
    try:
        from qgits.setup_verification import ensure_git_setup
        if not ensure_git_setup():
            print("Warning: Git setup verification failed. Some QGit features may not work correctly.")
    except Exception as e:
        print(f"Warning: Setup verification encountered an error: {e}")

def setup_requirements() -> List[str]:
    """Get setup requirements including setuptools and wheel."""
    return [
        "setuptools>=68.0.0",
        "wheel>=0.41.0",
        "python-dotenv>=1.0.0,<2.0.0",
    ]

def install_base_requirements():
    """Install base requirements before proceeding with setup."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "python-dotenv>=1.0.0,<2.0.0"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing base requirements: {e}")
        return False

def main():
    """Main setup function."""
    print("Setting up QGit...")
    
    # Install base requirements first
    if not install_base_requirements():
        print("Failed to install base requirements. Setup may not work correctly.")
    
    # Ensure basic setup requirements are installed
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + setup_requirements())
        print("✓ Setup requirements installed")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to install setup requirements: {e}")

    # Ensure environment directory and file exist
    ensure_env_directory()

    # Verify and install dependencies if needed
    if not verify_dependencies():
        print("Installing missing dependencies...")
        if not install_dependencies():
            print("Warning: Some dependencies may not be properly installed.")
        else:
            print("✓ Dependencies installed successfully")

    # Run setup verification
    run_setup_verification()
    
    # Create system-wide executable link
    create_system_link()
    
    print("\nQGit setup completed successfully!")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        with open("README.md", "r", encoding="utf-8") as fh:
            long_description = fh.read()

        setup(
            name="qgit",
            version="0.1.1",
            author="Griffin",
            author_email="griffin@griffin-code.com",
            description="A powerful Git operations automation tool with advanced security, visualization, and team insights",
            long_description=long_description,
            long_description_content_type="text/markdown",
            url="https://github.com/greyhatharold/qgit",
            packages=find_packages(),
            python_requires=">=3.8",
            classifiers=[
                "Development Status :: 4 - Beta",
                "Intended Audience :: Developers",
                "Topic :: Software Development :: Version Control :: Git",
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.13",
                "Operating System :: OS Independent",
                "Environment :: Console",
                "Environment :: X11 Applications :: GTK",
            ],
            install_requires=[
                # Core dependencies
                "pygame>=2.5.2,<3.0.0",
                "numpy>=1.26.0,<2.0.0",
                "PyOpenGL>=3.1.7,<4.0.0",
                "PyOpenGL-accelerate>=3.1.7,<4.0.0",
                "gitpython>=3.1.40,<4.0.0",
                "psutil>=5.9.6,<6.0.0",
                "python-dotenv>=1.0.0,<2.0.0",
            ],
            extras_require={
                'dev': [
                    "pytest>=7.4.3,<8.0.0",
                    "pytest-asyncio>=0.23.0,<1.0.0",
                    "pytest-cov>=4.1.0,<5.0.0",
                    "black>=23.11.0,<24.0.0",
                    "flake8>=6.1.0,<7.0.0",
                    "mypy>=1.7.0,<2.0.0",
                    "isort>=5.12.0,<6.0.0",
                ],
                'docs': [
                    "sphinx>=7.2.6,<8.0.0",
                    "sphinx-rtd-theme>=1.3.0,<2.0.0",
                ],
                'optional': [
                    "pillow>=10.1.0,<11.0.0",
                    "rich>=13.7.0,<14.0.0",
                    "tqdm>=4.66.1,<5.0.0",
                ],
            },
            entry_points={
                "console_scripts": [
                    "qgit=qgits.qgit:main",
                ],
            },
            package_data={
                "qgits": ["*.py", "setup_verification.py"],
            },
            include_package_data=True,
            keywords="git automation security visualization team-collaboration repository-management",
            project_urls={
                "Bug Reports": "https://github.com/griffinstrier/qgit/issues",
                "Source": "https://github.com/griffinstrier/qgit",
                "Documentation": "https://github.com/griffinstrier/qgit/docs",
            },
        ) 