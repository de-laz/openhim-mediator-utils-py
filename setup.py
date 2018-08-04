import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openhim_mediator_utils",
    version="0.0.2",
    author="Lazola Sifuba",
    author_email="sifubalazola@gmail.com",
    description="A utility library for build openHIM mediators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/de-laz/openhim-mediator-utils-py",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Developers"
    )
)
