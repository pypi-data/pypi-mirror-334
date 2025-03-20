import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="encryptionx",
    version="2.0.0",
    author="Mohammad Taha Gorji",
    author_email="MohammadTahaGorjiProfile@gmail.com",
    description="A comprehensive encryption library for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-r0ot/encryptionx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pycryptodome",
    ],
)
