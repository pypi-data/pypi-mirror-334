from setuptools import find_packages, setup

setup(
    name="WeatherUzbekistan",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests", "beautifulsoup4"
    ],
    author="Sino Farmonv",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    description="Bu o'zbekiston ob havosi haqida malumot beradigan kutubxona",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
)
