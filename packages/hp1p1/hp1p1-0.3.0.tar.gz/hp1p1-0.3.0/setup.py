from setuptools import setup, find_packages

setup(
    name="hp1p1",
    version="0.3.0",
    description="A very hp package",
    author="compinfun",
    author_email="compinfun@gmail.com",
    packages=find_packages(),
    package_data={
        "hp1p1": ["data/*.mp3"],
    },
    include_package_data=True,
)
