from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()
    
requirements = [
    "langdetect",
    "lingua-language-detector",
    "langid",
    "stanza",
    "fasttext-langdetect",
    "simplemma",
    "googletrans",
    "py-googletrans",
    "transformers",
    "torch",
    "pandas",
    "numpy",
    "boto3",
    "deepl",
    "sentencepiece",
    "fasttext",
    "huggingface_hub",
    "argostranslate",
]

setup(
    name="xtranslator",
    version="0.1.0",
    url="https://github.com/ivanvykopal/xtranslator.git",
    author="Ivan Vykopal",
    author_email="ivan.vykopal@gmail.com",
    python_requires=">=3.10.0",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    description="A package for translating text and detecting languages",
    packages=find_packages(),
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
)