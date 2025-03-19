from setuptools import setup, find_packages

setup(
    name="latex_generator_hse_spb_youka",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="Dmitriy Yukachev",
    author_email="dim.youka4@gmail.com",
    description="Библиотека для генерации LaTeX-кода таблиц и изображений",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Youka4/latex_gen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
