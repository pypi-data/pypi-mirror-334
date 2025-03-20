from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="suada",
    version="1.2.0-rc.1",
    author="Suada AI",
    author_email="hello@suada.ai",
    description="Official Python SDK for Suada's Business Analyst API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/accesslabs/python-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/accesslabs/python-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "langchain>=0.1.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
) 