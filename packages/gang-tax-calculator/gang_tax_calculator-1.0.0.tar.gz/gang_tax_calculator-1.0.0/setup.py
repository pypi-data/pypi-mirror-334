from setuptools import setup, find_packages

setup(
    name='gang_tax_calculator',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    author='gangadri yarraballi',
    description='A simple tax calculator package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
