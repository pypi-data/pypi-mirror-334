from setuptools import setup, find_packages
import pathlib

root = pathlib.Path(__file__).parent.resolve()
long_description_path = (root / "README.md").read_text(encoding="utf-8")

requirements_path = (root / "requirements.txt").read_text(encoding="utf-8")

setup(
    name="jam-tree",
    version="0.1.6",
    packages=find_packages(),
    install_requires=requirements_path,
    entry_points={
        "console_scripts": [
            "jam-tree=jam_tree.cli:cli",
        ],
    },
    author="Jordan Adelino",
    author_email="jordanadelino.info@gmail.com",
    description="Ferramenta para gerar árvore de diretórios com análise de IA",
    long_description=long_description_path,
    long_description_content_type="text/markdown",
    url="https://github.com/GitHubJordan/JAM-Tree",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: Portuguese (Brazilian)",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="jam-tree, setuptools, development, ai, analyzer, tree, directory, framework",
    project_urls={
        "Documentation": "https://jam-tree.readthedocs.io/",
        "Bug Reports": "https://github.com/GitHubJordan/JAM-Tree/issues",
        "Funding": "https://airtm.me/jordan_adelino",
        "Say Thanks!": "https://jordanadelino.info",
        "Source": "https://github.com/GitHubJordan/JAM-Tree/",
    },
)
