from setuptools import setup, find_packages

setup(
    name="unit_sphere_a_designs",
    version="0.1.0",
    description="A package for local search algorithms on unit sphere designs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aditya Pillai",
    author_email="aditya.pilai63916@gmail.com",
    url="https://github.com/adityapillai/unit_sphere_a_designs",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pytest",
        # Add other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
