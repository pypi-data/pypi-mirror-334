from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xss-detector",
    version="0.1.0",
    author="Yousuf",
    author_email="firedragonironfist998@gmail.com",
    description="A package for detecting XSS attacks using machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firedragonironfist/xss-detector",
    project_urls={
        "Bug Tracker": "https://github.com/firedragonironfist/xss-detector/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "tensorflow>=2.5.0",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.0",
        "flask>=2.0.0",
        "requests>=2.25.0",
        "kagglehub>=0.2.0"
    ],
    entry_points={
        "console_scripts": [
            "xss-detector=xss_detector.cli:main",
        ],
    },
)