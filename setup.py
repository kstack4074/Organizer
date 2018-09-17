from setuptools import setup, find_packages

setup(
    name='src',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'boto3',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
