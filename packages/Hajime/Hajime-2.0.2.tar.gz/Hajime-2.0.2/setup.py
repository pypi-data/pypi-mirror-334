from setuptools import setup, find_packages

setup(
    name="Hajime",
    version="2.0.2",
    packages=find_packages(),
    install_requires=['sqlalchemy', 'termcolor', 'websockets'],
    author="Franciszek Czajkowski",
    description="Lightweight Website Framework",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://Hajime.pythonanywhere.com",
    project_urls={
        "Source": "https://github.com/FCzajkowski/Hajime",
        "Documentation": "https://Hajime.pythonanywhere.com/Documentation"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)