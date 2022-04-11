import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coota",
    version="1.0.0",
    author="ATATC",
    author_email="futerry@outlook.com",
    description="A powerful data-generating library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atatc/coota",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "cupy", "matplotlib"],
    classifiers=[
        'Development Status :: 4 - Beta'
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
    ]
)
