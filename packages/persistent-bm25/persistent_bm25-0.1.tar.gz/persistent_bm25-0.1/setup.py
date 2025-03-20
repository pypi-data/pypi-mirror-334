from setuptools import setup, find_packages

setup(
    name="persistent_bm25",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain", "rank_bm25"
    ],
)
