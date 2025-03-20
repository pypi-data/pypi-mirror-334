from setuptools import setup, find_packages

setup(
    name="remnapi",
    version="0.1.19",
    packages=find_packages(),
    install_requires=[
        "certifi",
        "charset-normalizer",
        "idna",
        "python-dotenv",
        "requests",
        "shortuuid",
        "urllib3",
        "aiohttp"
    ],
    author="nvwrist",
    author_email="faxonq@gmail.com",
    description="API Remnawave for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nvwrist/remnapi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
