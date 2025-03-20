from setuptools import setup, find_packages

setup(
    name="pentit",
    version="1.0.9",
    author="Hussein Taha",
    author_email="contact@hussein.top",
    description="Universal Cybersecurity CLI Tool",
    long_description="""
    pentit is a lightweight yet powerful command-line cybersecurity tool designed for both 
    red team (offensive) and blue team (defensive) professionals. This tool provides essential 
    functionalities such as network scanning, IP tracking, encryption, WHOIS lookup, 
    subdomain enumeration, and system hardening.
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/HusseinTahaDEV/pentit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "pycryptodome",
        "python-whois",
        "argparse",
    ],
    entry_points={
    "console_scripts": [
        "pentit=pentit.main:main"
    ]
},
)