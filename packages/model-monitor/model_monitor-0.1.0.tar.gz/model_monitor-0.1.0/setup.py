from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="model-monitor",
    version="0.1.0",
    author="Biswanath Roul",
    author_email="biswanath.roul@example.com",
    description="A comprehensive library for automated model monitoring and drift detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biswanath-roul/model-monitor",
    project_urls={
        "Bug Tracker": "https://github.com/biswanath-roul/model-monitor/issues",
        "Documentation": "https://model-monitor.readthedocs.io",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(include=["model_monitor", "model_monitor.*"]),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "pydantic>=1.8.0",
        "PyYAML>=6.0",
        "joblib>=1.0.0",
        "tqdm>=4.62.0",
        "statsmodels>=0.13.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=0.910",
            "flake8>=4.0.0",
            "sphinx>=4.3.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "notification": [
            "slack-sdk>=3.15.0",
            "sendgrid>=6.9.0",
        ],
        "cloud": [
            "boto3>=1.20.0",
            "google-cloud-storage>=2.0.0",
            "azure-storage-blob>=12.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "model-monitor=model_monitor.cli:main",
        ],
    },
)