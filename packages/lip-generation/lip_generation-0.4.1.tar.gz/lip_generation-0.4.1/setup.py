from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='lip_generation',
    version='0.4.1',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
)