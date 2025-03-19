from setuptools import setup, find_packages

setup(
    name="py2pyd",
    version="0.1.0",
    license_file="LICENCE",
    packages=find_packages(),
    install_requires=["Cython"],
    entry_points={
      "console_scripts": [
        "py2pyd=py2pyd.compiler:convert"
    ]
    },
    author="Sacha Dehe",
    author_email="sachadehe@gmail.com",
    description="A simple and easy Python to PYD compiler using Cython",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sachadee/PythonPydGenerator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
