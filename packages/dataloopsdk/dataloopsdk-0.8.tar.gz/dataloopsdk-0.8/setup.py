import setuptools
from setuptools import find_packages

setuptools.setup(
    name="dataloopsdk",
    version="0.8",
    description="Python Package Boilerplate",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    author="ivan",
    python_requires=">=3.6",
    author_email="ivan.liu@anker-in.com",
    url="",
    # py_modules=['sdk'],
    install_requires=[
        "requests==2.31.0",
        "pydantic==2.9.2",
        "hachoir==3.3.0",
        "httpx==0.27.1"
    ],
    license="MIT License",
    zip_safe=False,
    keywords="",
    packages=find_packages(),
)
