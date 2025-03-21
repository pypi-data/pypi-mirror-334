from setuptools import setup, find_packages

setup(
    name="VulnScanX",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Kamil Rahuman",
    author_email="kamilrahman32@gmail.com",
    description="A vulnerability scanner tool",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KamilRahuman/VulnScanX",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
