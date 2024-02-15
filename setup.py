from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in demo14/__init__.py
from demo14 import __version__ as version

setup(
	name="demo14",
	version=version,
	description="Demo",
	author="Viral Patel",
	author_email="viral@fosserp.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
