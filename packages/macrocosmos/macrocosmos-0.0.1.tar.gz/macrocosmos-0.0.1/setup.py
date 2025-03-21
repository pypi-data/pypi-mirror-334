from setuptools import setup, find_packages

setup(
    name="macrocosmos",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        # For example:
        # "requests>=2.25.1",
        # "pandas>=1.2.0",
    ],
    author="Macrocosmos",
    author_email="support@macrocosmos.ai",
    description="SDK for Macrocosmos API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/macrocosm-os/macrocosmos-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)