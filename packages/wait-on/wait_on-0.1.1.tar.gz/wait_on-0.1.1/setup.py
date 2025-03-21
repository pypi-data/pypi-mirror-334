from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wait-on",
    version="0.1.1",
    description="Utilitário para aguardar recursos como arquivos, portas, sockets e HTTP(S)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Devin AI",
    author_email="devin-ai-integration[bot]@users.noreply.github.com",
    url="https://github.com/keviocastro/wait-on",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wait-on=python_wait_on.cli:main",
        ],
    },
    install_requires=[
        "requests>=2.25.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    keywords="wait, resources, synchronization, utility, cli",
)
