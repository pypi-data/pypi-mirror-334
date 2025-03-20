from setuptools import setup, find_packages

setup(
    name="magnetic_transform",  # Package name (must be unique on PyPI)
    version="0.1",  # Package version
    description="A library for magnetic field transformation",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/magnetic_transform",  # GitHub link (optional)
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
