from setuptools import setup, find_packages

setup(
    name="callai",
    version="0.2.0",
    description="一个简单的OpenAI API兼容封装库",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/callai",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "httpx>=0.23.0",
    ],
    extras_require={
        "socks": ["httpx[socks]"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
    keywords="openai, ai, gpt, api, client, wrapper",
) 