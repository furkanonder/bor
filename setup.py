from pathlib import Path

from setuptools import setup

CURRENT_DIR = Path(__file__).parent


def get_long_description():
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name="bor",
    version="0.0.1",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    description="User-friendly, tiny source code searcher written by pure Python.",
    keywords=["code searcher"],
    author="Furkan Onder",
    author_email="furkanonder@protonmail.com",
    url="https://github.com/furkanonder/bor/",
    license="MIT",
    python_requires=">=3.0",
    py_modules=["bor"],
    install_requires=[],
    extras_require={},
    zip_safe=False,
    include_package_data=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix ",
    ],
    entry_points={
        "console_scripts": [
            "bor = bor:main",
        ],
    },
)
