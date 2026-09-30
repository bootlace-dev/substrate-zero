from setuptools import setup, find_packages

setup(
    name="substrate-zero",
    version="0.1.0",
    description="The Full-Stack Cryptographic Substrate & Ephemeral Secret Failure Testbed",
    author="bootlace-dev",
    author_email="bootlace-dev@users.noreply.github.com",
    url="https://github.com/bootlace-dev/substrate-zero",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "click>=8.0.0",
        "ecdsa>=0.18.0",
    ],
    entry_points={
        "console_scripts": [
            "substrate-zero=substrate_zero.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
)
