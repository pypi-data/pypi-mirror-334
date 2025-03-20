from setuptools import setup, find_packages

setup(
    name='lwc_utils',
    version='0.0.1',
    description='LWC Utils',
    author='LWC',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
    ],
    python_requires='>=3.6',
)