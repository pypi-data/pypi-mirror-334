from setuptools import setup, find_packages

with open(r"C:\Users\y\Desktop\encrypt_data\README.md", 'r') as file:
    description = file.read()

setup(
    name='encrypt_data',
    version='0.2',
    packages=find_packages(),
    install_requires=['cryptography', 'rsa'],
    long_description=description,
    long_description_content_type="text/markdown",
)