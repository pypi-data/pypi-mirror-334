from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agent-mont",
    version="0.1.2",
    author="Faisal (BizTech)",
    author_email="faisalazeeii786@gmail.com",
    description="A comprehensive monitoring solution for AI agent frameworks including Langchain, CrewAI, and Agno. AgentMont provides enhanced metrics and deep observability for production AI agent applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ansarifaisal12/Agent_Monts.git",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "psutil",
        "matplotlib",
        "streamlit",
        "tiktoken"
    ],
    include_package_data=True,
)
