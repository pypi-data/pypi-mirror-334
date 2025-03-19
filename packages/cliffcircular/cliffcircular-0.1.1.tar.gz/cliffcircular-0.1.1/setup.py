from setuptools import setup, find_packages
import os

# Read the contents of README file for the long description.
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cliffcircular",
    version="0.1.1",
    description="A custom Gymnasium gridworld environment for testing SafeRL algorithms for partially observable Constrained Submodular Markov Decision Processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zihan Wang",
    author_email="wang5044@purdue.edu",
    url="https://github.com/EdisonPricehan/CliffCircular",
    license="GPLv3",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cliffcircular": ["img/*.png"],
    },
    install_requires=[
        "gymnasium>=0.26.0",
        "numpy>=1.21.0",
        "pygame>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Or Beta/Production/Stable as appropriate
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
