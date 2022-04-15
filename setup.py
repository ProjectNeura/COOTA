import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="coota",
    version="1.0.0b3",
    author="ATATC",
    author_email="futerry@outlook.com",
    description="A powerful data-generating library.",
    license='Apache License 2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atatc/coota",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "matplotlib"],
)
