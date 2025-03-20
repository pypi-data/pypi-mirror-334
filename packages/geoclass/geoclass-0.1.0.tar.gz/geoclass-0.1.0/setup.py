from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geoclass",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python module for satellite image classification and land valuation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/geoclass",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "tensorflow>=2.8.0",
        "opencv-python>=4.5.0",
        "rasterio>=1.2.0",
        "geopy>=2.2.0",
        "scikit-learn>=0.24.0",
        "requests>=2.26.0",
        "beautifulsoup4>=4.9.0",
        "selenium>=4.0.0",
        "pillow>=8.0.0",
        "matplotlib>=3.4.0",
        "pytest>=6.2.0",
        "python-dotenv>=0.19.0",
        "pyproj>=3.1.0",
        "shapely>=1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "black>=21.7b0",
            "isort>=5.9.3",
            "flake8>=3.9.2",
            "mypy>=0.910",
        ],
    },
) 