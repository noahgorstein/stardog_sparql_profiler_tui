from setuptools import setup, find_packages

setup(
    name="sparql-profiler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": [
            "sparql-profiler = cli:query_profiler_app",
        ],
    },
)
