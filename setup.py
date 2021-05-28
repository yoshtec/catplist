import setuptools

VERSION = "0.0.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="catplist",
    version=VERSION,
    author="Yoshtec",
    author_email="yoshtec@gmail.com",
    description="Display apple plist files in a readable and comprehensible way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoshtec/catplist",
    entry_points={"console_scripts": ["catplist = catplist.catplist:catplist"]},
    packages=setuptools.find_packages(),
    install_requires=["click"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
    ],
    keywords="plist, ios, iphone, ipad",
    python_requires=">=3.5",
)
