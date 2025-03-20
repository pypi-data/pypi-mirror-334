from setuptools import setup, find_packages

setup(
    name="aisystems",
    version="0.1.0",
    packages=find_packages(include=['aisystems', 'aisystems.*']),
    description="A Python package for AI systems",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Ayush Chaurasia",
    author_email="ayush.chaurarsia@gmail.com",
    url="https://github.com/ayushexel/aisystems",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Add your package dependencies here
    ],
)