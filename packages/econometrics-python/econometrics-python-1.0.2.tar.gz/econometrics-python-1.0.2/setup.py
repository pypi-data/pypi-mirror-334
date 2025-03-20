from setuptools import setup, find_packages

setup(
    name='econometrics-python',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'statsmodels',
        'matplotlib'
    ],
    description='Package for econometric.',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='Trần Minh Tâm',
    author_email='tam.ming.zhan@gmail.com',
    url='https://github.com/Trantamming/econometrics',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
