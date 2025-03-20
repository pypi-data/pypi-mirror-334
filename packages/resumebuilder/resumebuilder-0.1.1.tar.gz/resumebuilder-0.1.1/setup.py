from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()
    # Remove comments from requirements
    requirements = [r.split('#')[0].strip() for r in requirements if r.split('#')[0].strip()]

# Development dependencies
dev_requires = [
    "pytest>=7.3.1",
    "pytest-cov>=4.1.0",
    "flake8>=6.0.0",
    "black>=23.3.0",
    "isort>=5.12.0",
    "mypy>=1.3.0",
    "build>=0.10.0",
    "twine>=4.0.2",
]

setup(
    name="resumebuilder",
    version="0.1.1",
    author="Brad Jackson",
    author_email="me@brad-jackson.com",
    description="A professional resume and cover letter generator with templating and customization options",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iron-hope-shop/tools-resume",
    project_urls={
        "Bug Tracker": "https://github.com/iron-hope-shop/tools-resume/issues",
        "Documentation": "https://github.com/iron-hope-shop/tools-resume/blob/master/README.md",
        "Source Code": "https://github.com/iron-hope-shop/tools-resume",
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "resumebuilder": [
            "resources/fonts/*", 
            "resources/images/*", 
            "templates/*/*/*",  # Include all files in all subdirectories
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    keywords="resume, cv, cover letter, pdf, generator, template, job application",
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": dev_requires,
    },
    entry_points={
        "console_scripts": [
            "resumebuilder=resumebuilder.cli.main:main",
        ],
    },
) 