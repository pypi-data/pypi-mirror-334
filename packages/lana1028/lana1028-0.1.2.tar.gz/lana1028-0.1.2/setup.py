from setuptools import setup, find_packages

setup(
    name="lana1028",
    version="0.1.2",
    author="Tristan",
    author_email="contactpgag@gmail.com",
    description="LANA-1028: A custom encryption algorithm.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lana1028",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
