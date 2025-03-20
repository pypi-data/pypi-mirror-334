from setuptools import setup, find_packages

setup(
    name="bluetoof",
    version="0.2.0",
    description="Librairie Python pour interagir avec des appareils Bluetooth",
    author="mz4r",
    author_email="mz4rr@proton.me",
    packages=find_packages(),
    install_requires=["pybluez"],
)