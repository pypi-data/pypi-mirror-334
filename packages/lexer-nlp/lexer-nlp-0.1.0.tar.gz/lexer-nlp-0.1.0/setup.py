from setuptools import setup, find_packages

setup(
    name="lexer-nlp",  # Package name
    version="0.1.0",  # Version number
    description="A Python package to display text/docs in the terminal.",
    author="SeventyThree",
    author_email="73@gmail.com",
    packages=find_packages(),  # Automatically find packages
    include_package_data=True,  # Include non-Python files (e.g., text files)
    package_data={
        "lexer": ["data/*.txt"],  # Include all .txt files in the data folder
    },
    install_requires=[],  # Add dependencies if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python version requirement
)