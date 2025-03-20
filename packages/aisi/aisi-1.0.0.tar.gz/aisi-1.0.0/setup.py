from setuptools import setup, find_packages

setup(
    name="aisi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "clight",
        
    ],
    entry_points={
        "console_scripts": [
            "aisi=aisi.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "aisi": [
            "main.py",
            "__init__.py",
            "__system__/imports.py",
            "__system__/index.py",
            "__system__/modules/jobs.py",
            "__system__/sources/clight.json"
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="Pending",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        
        "Operating System :: OS Independent",
    ],
)
