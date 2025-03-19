from setuptools import setup

setup(
    name="aiopandas",
    version="0.0.1",
    packages=["aiopandas"],
    install_requires=["pandas"],
    author="Elias Neuman",
    author_email="elias@payperrun.com",
    description="Lightweight Pandas monkey-patch for async map, apply, transform, etc.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/telekinesis-inc/aiopandas",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
