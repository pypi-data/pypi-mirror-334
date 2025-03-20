from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="codoniser",
    version="1.0.1",
    author="Thomas J. Booth",
    author_email="thoboo@biosustain.dtu.dk",
    packages=find_packages(),
    description="A python package to analyse and optimise codons.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrBoothTJ/codoniser",
    license='GNU General Public License v3.0',
    python_requires='>=3.7',
    install_requires=[
      'biopython>=1.83',
      'matplotlib>=3.10.0',
      'seaborn>=0.13.2',
      'scipy>=1.15.1'
    ],
    entry_points={'console_scripts': ["codoniser=codoniser.main:main"]}
)
