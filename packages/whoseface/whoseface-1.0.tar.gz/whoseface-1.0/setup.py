from setuptools import setup, find_packages

setup(
    name="whoseface",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "face_recognition"
    ],
)
