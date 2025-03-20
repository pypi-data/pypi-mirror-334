from setuptools import setup, find_packages

setup(
    name="cross-service-auth",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "djangorestframework",
        "djangorestframework-simplejwt",
    ],
    description="Package for authentication between microservices",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
