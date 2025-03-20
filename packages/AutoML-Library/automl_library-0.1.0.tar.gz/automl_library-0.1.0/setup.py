from setuptools import setup, find_packages

setup(
    name="AutoML_Library",
    version="0.1.0",
    author="Arnav Upadhyay",
    author_email="upadhyayarnav2004@gmail.com",
    description="An advanced AutoML library with dataset visualization and ML algorithms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MASKED-GOD/AutoML_Library",
    packages=find_packages(),
    install_requires=[
        "numpy", "pandas", "scikit-learn", "matplotlib", "seaborn",
        "xgboost", "lightgbm", "catboost"
    ],
    license="MIT",  # 👈 Added License
    classifiers=[
        "License :: OSI Approved :: MIT License",  # 👈 Added Classifier
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)
