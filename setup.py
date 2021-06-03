from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Operations Research Models & Methods (ORMM) is inspired by Paul A. Jensen's
Excel Add-ins.  His Excel packages were last updated in 2011, and while I
believe they do still work, his work may become outdated in a couple of ways:

- Excel is not as commonly used for OR, except in settings where security is
  of the utmost concern and/or modern languages like Python, R, Julia, C, C++,
  MATLAB, AMPL, or other modeling software are not available.
- From what I understand, Microsoft has been trying to phase out VBA and move
  to Javascript.  If this happens, this could significantly impact whether or
  not his packages will work.
- While his website and packages are still available
  `here <https://www.me.utexas.edu/~jensen/ORMM/>`_, some sections are/may
  become unusable.  The animations rely on Flash, which is being phased out
  in google chrome and other web browsers.

This python package aims to accomplish some of the same goals as Paul
Jensen's website and add-ins did, mainly to

1. Be an educational tool that shows how abstract models (linear programs,
   integer programs, nonlinear programs, etc.) can be applied to real-life
   scenarios to solve complex problems.
2. Help the practitioner by providing modeling frameworks, methods for solving
   these models, and problem classes so a user can more easily see how they
   may be able to frame their business problem/objective through the lens of
   Operations Research.

This repository contains subpackages for grouping the different types of OR
Models & Methods.  Currently this subpackage list includes

1. `mathprog`: A subpackage for mathematical programs, including linear
   programs and mixed integer linear programs.
2. `markov`: A subpackage for discrete state markov analysis.
3. `network`: A subpackage for network models and methods, including the
   transportation and shortest path tree problems.
"""

PROJECT_URLS = {
    "Documentation": "https://ormm.readthedocs.io/en/stable/",
}

setup(
    name="ormm",
    version="0.1.0",
    description="A collection of Operations Research Models & Methods",
    url="https://github.com/egbuck/ormm",
    author="Ethan Buck",
    author_email="egbuck96@gmail.com",
    packages=find_packages(include=["ormm", "ormm.*"]),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    install_requires=[
        "pyomo >= 5.0",
        "pandas >= 1",
        "quantecon >= 0.4"
    ],
    extras_require={
        "dev": [
            "pytest >= 6.0",
            "sphinx >= 3.1.2",
            "sphinx_rtd_theme >= 0.5.0",
            "twine >= 3.2.0",
            "flake8 >= 3.8.3",
            "pytest-cov >=2.10.0",
            "codecov >= 2.1.8"
            # "check-manifest>=0.42" # used for creating Manifest.in
        ]
    },
    classifiers=[
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        ("License :: OSI Approved :: "
         "GNU General Public License v3 or later (GPLv3+)"),
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    project_urls=PROJECT_URLS,
)
