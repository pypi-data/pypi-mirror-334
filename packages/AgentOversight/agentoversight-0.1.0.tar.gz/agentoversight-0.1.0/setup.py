from setuptools import setup, find_packages

setup(
    name="AgentOversight",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.3.3",
        "nltk>=3.8.1",
        "openai>=1.10.0",
        "requests>=2.31.0",
        "textblob>=0.18.0",
        "httpx>=0.27.0",  
    ],
    include_package_data=True,
    package_data={
        "AgentOversight": ["templates/*.html"],  # Include Flask templates
    },
    author="Logeswaran",
    author_email="loks2cool@gmail.com",
    description="A tool to oversee and evaluate agentic AI performance with validation and guidance",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/loks2cool/AgentOversight",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "agent-oversight=AgentOversight.app:main",  # Command-line entry for Flask app
        ],
    },
)