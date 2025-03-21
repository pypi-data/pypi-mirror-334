from setuptools import setup, find_packages

setup(
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "opensubmarine": ["py.typed"],
        "opensubmarine.contracts.access.Ownable": ["*.pyi"],
        "opensubmarine.contracts.participation.Stakable": ["*.pyi"],
        "opensubmarine.contracts.update.Upgradeable": ["*.pyi"],
        "opensubmarine.contracts.token.ARC200": ["src/*.pyi"],
    },
    zip_safe=False,  # Required for mypy to find py.typed files
)
