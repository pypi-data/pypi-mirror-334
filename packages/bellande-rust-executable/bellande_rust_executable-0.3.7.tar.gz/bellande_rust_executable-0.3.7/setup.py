from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bellande_rust_executable",
    version="0.3.7",
    description="Bellande Rust Executable is a library that makes rust code into an executable (BRE) library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RonaldsonBellande",
    author_email="ronaldsonbellande@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
    ],
    keywords=["package", "setuptools"],
    python_requires=">=3.0",
    extras_require={
        "dev": ["pytest", "pytest-cov[all]", "mypy", "black"],
    },
    entry_points={
        'console_scripts': [
            'bellande_rust_executable = bellande_rust.bellande_rust_executable:main',
        ],
    },
    project_urls={
        "Home": "https://github.com/Architecture-Mechanism/bellande_rust_executable",
        "Homepage": "https://github.com/Architecture-Mechanism/bellande_rust_executable",
        "documentation": "https://github.com/Architecture-Mechanism/bellande_rust_executable",
        "repository": "https://github.com/Architecture-Mechanism/bellande_rust_executable",
    },
)
