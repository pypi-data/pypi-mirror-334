import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="book-return-lib",
    version="0.0.1",
    author="Alfi",
    author_email="alfithomas2002@gmail.com",
    description="A library for calculating book return due dates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/book-return-lib",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
