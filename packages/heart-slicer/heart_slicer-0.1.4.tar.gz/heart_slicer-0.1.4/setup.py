from setuptools import setup, find_packages

setup(
    name="heart_slicer",
    version="0.1.4",
    description=
    """A package to process images of heart slices for analyses.""",
    author="True Galaxus",
    author_email="ron.reclame@gmail.com",
    packages=find_packages(),
    install_requires=["numpy", "pillow", "pyyaml", "matplotlib"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    # files to include are defined in MANIFEST.in
)