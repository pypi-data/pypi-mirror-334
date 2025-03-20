from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="openai-streamer",  # Use hyphens instead of underscores for PyPI
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
    ],
    author="Serge",
    author_email="your.email@example.com",
    description="A package for streaming text completion using OpenAI's Responses API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openai-streamer",  # Update with your actual repository URL
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/openai-streamer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    keywords="openai, ai, streaming, text completion, gpt",
)
