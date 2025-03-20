from setuptools import setup, find_packages

setup(
    name='rmbi3110',
    version='1.2.9',
    description='Do not distribute it without permission. ',
    author='Xuhu Wan',
    author_email='xuhu.wan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
        'yfinance',
        'statsmodels'
    ],
)
