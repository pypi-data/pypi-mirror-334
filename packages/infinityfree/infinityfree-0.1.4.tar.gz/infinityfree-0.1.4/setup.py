from setuptools import setup, find_packages

setup(
    name="infinityfree",
    version="0.1.4",
    author="Rakhilukky",
    author_email="lukkyrakhi@gmail.com",
    description="A module to bypass InfinityFree API security checks for Scraping or API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Rakhilukky/infinityfree",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pycryptodome"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
