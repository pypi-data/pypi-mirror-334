from setuptools import setup, find_packages

setup(
    name="heart_slicer",
    version="0.2.0",
    description=
    """A package to process images of coloured histology sections of the heart for analyses.""",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="True Galaxus",
    author_email="truegalaxus@gmail.com",
    packages=find_packages(),
    install_requires=["numpy", "pillow", "pyyaml", "matplotlib"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    # files to include are defined in MANIFEST.in
)