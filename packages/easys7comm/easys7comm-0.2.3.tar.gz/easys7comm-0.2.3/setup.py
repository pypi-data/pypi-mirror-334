from setuptools import setup, find_packages

setup(
    name="easys7comm",
    version="0.2.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)