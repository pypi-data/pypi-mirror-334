from setuptools import setup, find_packages
import os

# READMEへの絶対パスを取得
readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")

with open(readme_path, "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pylogiless",
    version="0.1.0",
    author="LOGILESS API Python Client Contributors",
    author_email="contact@logiless.jp",
    description="Python client for the LOGILESS API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/logiless/pylogiless",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "requests-oauthlib>=1.3.0",
    ],
    keywords="logiless, api, logistics, inventory, warehouse",
    project_urls={
        "Bug Tracker": "https://github.com/logiless/pylogiless/issues",
        "Documentation": "https://github.com/logiless/pylogiless/blob/main/docs",
        "Source Code": "https://github.com/logiless/pylogiless",
    },
)
