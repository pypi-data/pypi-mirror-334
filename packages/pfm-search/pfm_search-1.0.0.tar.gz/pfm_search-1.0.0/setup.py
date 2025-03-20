from setuptools import setup

setup(
    name="pfm-search",  # Unique package name
    version="1.0.0",  # Update this for new versions
    description="A Python module for fetching search results from PFM-Search",
    author="Krushna",
    author_email="your-email@example.com",  # Use a real email
    py_modules=["pfm_search"],  # The Python module file
    install_requires=["requests"],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
