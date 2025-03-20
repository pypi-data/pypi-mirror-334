from setuptools import setup

# , find_packages


setup(
    name="luadata.luatable",
    version="0.0.3",
    description="Lua Table wrapper for serializing",
    summary="Lua Table",
    license="GPLv3",
    url="https://github.com/huakim/python-luadata.luatable",
    packages=["luadata.luatable"],
    install_requires=["luadata", "lupa"],
)
