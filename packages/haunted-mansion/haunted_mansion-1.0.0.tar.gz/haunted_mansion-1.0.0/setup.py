from setuptools import setup, find_packages

setup(
    name="haunted_mansion",
    version="1.0.0",
    author="Karthikeya",
    author_email="karthikeyaa.official@gmail.com",
    description="A text-based adventure game set in a haunted mansion.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "emoji",
    ],
    entry_points={
        "console_scripts": [
            "haunted-mansion=haunted_mansion.game:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)