import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cezve",  # Replace with your own username
    version="0.0.1",
    author="Emerson Max de Medeiros Silva",
    author_email="emersonmx@gmail.com",
    description="A really small web framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emersonmx/cezve",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
