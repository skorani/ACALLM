from setuptools import setup, find_packages

setup(
    name='my_python_project',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',  # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'my_python_project=src.main:main',
        ],
    },
)
