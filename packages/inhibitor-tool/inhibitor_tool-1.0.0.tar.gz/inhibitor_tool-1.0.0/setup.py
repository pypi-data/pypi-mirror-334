from setuptools import setup, find_packages
import io

setup(
    name="inhibitor_tool",
    version="1.0.0",
    author="mengmengwei",
    author_email="mmwei3@iflytek.com,+8617855350258",
    description="A tool for adding items to the inhibition list via API",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pwxwmm/inhibitor_tool",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "inhibitor-tool=inhibitor_tool.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
