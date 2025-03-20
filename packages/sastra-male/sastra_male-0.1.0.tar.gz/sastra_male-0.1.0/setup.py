from setuptools import setup, find_packages

setup(
    name="sastra-male",
    version="0.1.0",
    author="Jeevakrishna.V",
    author_email="jeevakrishna073@gmail.com",
    description="A package for KNN analysis with PCA in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jeevakrishna/sastra-male",  # Replace with actual repo
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
