from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="microgue",
    version="4.1.0",
    author="Michael Hudelson",
    author_email="michaelhudelson@gmail.com",
    description="This project contains bootstrap code to speed up the development of AWS based microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=[
        "microgue",
        "microgue.caches",
        "microgue.events",
        "microgue.loggers",
        "microgue.models",
        "microgue.queues",
        "microgue.secrets",
        "microgue.services",
        "microgue.storages",
    ],
    install_requires=[
        "aioboto3",
        "boto3",
        "httpx",
        "redis",
        "requests",
    ],
    python_requires=">=3.10",
)
