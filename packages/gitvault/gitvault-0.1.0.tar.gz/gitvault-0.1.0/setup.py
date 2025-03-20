from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitvault",
    version="0.1.0",
    author="Ayush Kumar",
    author_email="ayushkumar1221@gmail.com",
    description="A package for secure data encryption and decryption with Git integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayush1920/GitValult",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "cryptography",
        "GitPython",
        "pytest",
        "python-dotenv",
        "requests",
        "setuptools",
        "urllib3"
    ],
)