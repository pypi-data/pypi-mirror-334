from setuptools import setup, find_packages
import sys
import platform


setup(
    name="py2pyd",
    version="0.1.2",
    license_file="LICENCE",
    packages=find_packages(),
    install_requires=["Cython", "setuptools"],
    entry_points = {
      "console_scripts": ["py2pyd=py2pyd:convert"]
    },
    author="Sacha Dehe",
    author_email="sachadehe@gmail.com",
    description="Cross-platform .py file to shared library compiler, .pyd (Windows) or .so (Linux).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sachadee/PythonPydGenerator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
