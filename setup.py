import setuptools

setuptools.setup(
    name="coota",
    version="1.0.3",
    author="ATATC",
    author_email="futerry@outlook.com",
    description="A powerful data-generating library.",
    license='Apache License 2.0',
    long_description="**COOTA**(Come Out Of Thin Air) is a powerful data-generating python library. "
                     "By supporting generator nesting, it allows you to generate a variety of data "
                     "that shows great randomness. It also supports making generators conform to a "
                     "certain distribution and associating two generators.",
    long_description_content_type="text/markdown",
    url="https://github.com/ATATC/COOTA",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "matplotlib", "scipy"],
)
