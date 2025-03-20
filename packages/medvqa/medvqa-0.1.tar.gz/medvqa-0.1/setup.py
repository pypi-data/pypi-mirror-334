from setuptools import setup, find_packages

setup(
    name='medvqa',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'medvqa=medvqa.cli:main',
        ],
    },
    install_requires=[
        # Add your dependencies here
    ],
)
