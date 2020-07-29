from setuptools import setup, find_packages

setup(
    name = "ormm",
    version = "0.0.1",
    description = "Operations Research Models & Methods",
    packages = find_packages(include=["ormm", "ormm.*"]),
    #packages = find_packages(include="ormm"),
    #py_modules = ["opt"],
    #package_dir = {"":"ormm"},
    install_requires = [
        "pyomo >= 5.0",
    ],
    extras_require = {
        "dev": [
            "pytest >= 6.0",
            "sphinx >= 3.1.2",
            "sphinx_rtd_theme >= 0.5.0",
        ]
    },
)