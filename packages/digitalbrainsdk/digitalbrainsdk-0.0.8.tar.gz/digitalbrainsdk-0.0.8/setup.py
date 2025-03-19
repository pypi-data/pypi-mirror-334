from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-8') as f:
    required = f.read().splitlines()

setup(
    name="digitalbrainsdk",
    version="0.0.8",
    author="XingLi",
    author_email="lihouxing@yeah.net",
    description="A Python SDK for Digital Brain analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "digitalbrainsdk": ["config.ini"],
    },
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
