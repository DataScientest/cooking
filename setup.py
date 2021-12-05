import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="cooking",
    version="1.0.0",
    url="",
    license="BSD",
    maintainer="Oussama Derouiche",
    maintainer_email="oussama.derouiche96@gmail.com",
    description="The basic cooking app app built Datascientist.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)
