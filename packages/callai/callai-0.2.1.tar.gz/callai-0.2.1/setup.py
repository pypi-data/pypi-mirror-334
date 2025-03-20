from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="callai",
    version="0.2.1",
    author="AI中文开发者",
    author_email="aixiasang@163.com",
    description="一个简单的OpenAI API兼容封装库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aixiasang/callai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "openai>=1.0.0",
        "httpx",
    ],
) 