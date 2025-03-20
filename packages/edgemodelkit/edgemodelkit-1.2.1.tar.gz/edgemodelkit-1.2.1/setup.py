from setuptools import setup, find_packages
import codecs
import os

# Get the directory containing this file
here = os.path.abspath(os.path.dirname(__file__))

# Read the README file for the long description
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

# Define the package version
VERSION = "1.2.1"  # Initial version for edgemodelkit

# Package description
DESCRIPTION = "edgemodelkit: A Python library for seamless sensor data acquisition and logging."
LONG_DESCRIPTION = (
    "edgemodelkit is a Python library developed by EdgeNeuron, designed for efficient sensor data acquisition, "
    "real-time processing, and logging. The library integrates with edge devices to streamline data pipelines for "
    "machine learning and IoT applications."
)

# Define the setup configuration
setup(
    name="edgemodelkit",  # Unique package name for edgemodelkit
    version=VERSION,
    author="EdgeNeuron",
    author_email="official@consentiumiot.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ConsentiumIoT/edgemodelkit",  # Repository URL
    packages=find_packages(),  # Automatically discover all packages
    install_requires=[
        "numpy",  # For numerical operations
        "pandas",  # For data logging and manipulation
        "pyserial",  # For serial port communication
        "tensorflow",  # If required for ML integrations
        "tqdm",          # For progress bar
        "joblib"        # For pickle file
    ],
    extras_require={
        "dev": [
            "pytest",  # Testing framework for development
            "flake8",  # Linter for code quality
            "black",  # Code formatter
        ]
    },
    keywords=[
        "Python",
        "Edge Computing",
        "IoT",
        "Sensor Data",
        "Data Logging",
        "EdgeNeuron",
        "edgemodelkit",
        "Machine Learning",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # Updated to Beta for edgemodelkit
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Specify the minimum supported Python version
    project_urls={
        "Bug Tracker": "https://github.com/ConsentiumIoT/edgemodelkit/issues",
        "Documentation": "https://github.com/ConsentiumIoT/edgemodelkit#readme",
        "Source Code": "https://github.com/ConsentiumIoT/edgemodelkit",
    },
)
