from setuptools import setup, find_packages
import os
# Read the README.md file
current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="request_sentinal",
    version="1.2.0",
    packages=find_packages(),
    install_requires=["requests"],
    description="A Python Package for web scrapers to scrape the world without worrying about rate limits.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Santhosh T K",
    author_email="22z433@psgtech.ac.in",
    url="https://github.com/santhoshtk01/request_sentinal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # Include non-Python files (e.g., config.json)
    package_data={
        "rate_limiter": ["config.json"],  # Include config.json in the package
    },
    python_requires=">=3.7",
)