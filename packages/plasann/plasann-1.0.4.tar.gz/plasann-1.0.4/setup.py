from setuptools import setup, find_packages

setup(
    name="plasann",
    version="1.0.4",
    author="Habibul Islam",
    author_email="hislam2@ur.rochester.edu",
    description="A plasmid annotation pipeline",
    packages=find_packages(),
    install_requires=[
        "biopython",
        "pandas",
        "matplotlib",
        "pycirclize",
        "gdown",
    ],
    entry_points={
        "console_scripts": [
            "PlasAnn=plasann.cli:main",
        ],
    },
)