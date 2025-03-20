from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="DualNet-TCM",
    version="0.1a8",
    description="DualNet-TCM：分别从中医和西医维度对中药进行“以靶找药”和“以药找靶”的新型中药网络药理学",
    # Optional
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MLi-lab-Bioinformatics-NJUCM/HerbiV",
    author="沈天威、胡屹莹",
    author_email="2990834217@qq.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    keywords="network pharmacology",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
                      "numpy",
                      "pandas",
                      "tqdm",
                      "pyecharts"
                      ],
    project_urls={
        "Bug Reports": "https://github.com/Carrie-HuYY/DualNet-TCM/issues",
        "Source": "https://github.com/Carrie-HuYY/DualNet-TCM",
    },
)