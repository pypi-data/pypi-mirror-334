from setuptools import setup, find_packages

setup(
    name="PygameEnhanced",
    version="1.4.3",
    packages=find_packages(),
    include_package_data=True,
    package_data={"PygameEnhanced": ["templates/*.html"]},
    install_requires=[
        "Flask",
        "setuptools"  # Required for pkg_resources
    ],
)
