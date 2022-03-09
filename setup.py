from setuptools import setup, version

setup(
    name="FlowCalc",
    version="0.0",
    author="William E. Robinson",
    packages = ["FlowCalc"],
    install_requires=[
        "numpy >= 1.21.1",
        "tomli >= 2.0.1",
        "tomli-w >= 1.0.0",
    ],
)
