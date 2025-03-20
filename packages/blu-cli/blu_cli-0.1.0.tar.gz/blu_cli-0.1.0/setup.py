from setuptools import setup, find_packages

setup(
    name="blu-cli",
    version="0.1.0",
    description="Automate the entire Software Development Lifecycle.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Stratum Labs",
    author_email="hq@stratumlabs.ai",
    url="https://github.com/dj-io/blu",
    project_urls={
        "Code": "https://github.com/dj-io/blu",
        "Documentation": "https://github.com/dj-io/blu/blob/main/blu-cli/README.md",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=[
        "questionary",
        "click",
        "python-dotenv",
        "halo",
        "flake8",
        "black",
    ],
    extras_require={
        "dev": ["pytest"],
    },
    entry_points={
        "console_scripts": [
            "blu=blu.main:blu",  # Maps the `blu` command to the `blu()` group function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
)
