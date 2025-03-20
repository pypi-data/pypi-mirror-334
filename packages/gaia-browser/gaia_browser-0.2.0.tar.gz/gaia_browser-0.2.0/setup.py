from setuptools import setup, find_packages

setup(
    name="gaia-browser",
    version="0.2.0",
    author="Ma Weiyi",
    author_email="fwyr@proton.me",
    license="MIT",
    description="the terminal-living library genesis browser",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fwyr/gaia",
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich",
        "beautifulsoup4",
        "pyfiglet"
    ],
    entry_points={
        "console_scripts": [
            "gaia=gaia.cli:main",  # Adjust this to point to your main function
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
