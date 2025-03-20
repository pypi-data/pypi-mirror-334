from setuptools import setup,find_packages

setup(
	name = "siddhis_indian_states_25",
	version = "0.1",
	packages=find_packages(),
	include_package_data = True,
	install_requires = ["django"],
	license="MIT",
	description = "A Django app that provides Indian State choices as a model and form field.",
	author = "Siddhi Ramesh Sutar",
	author_email = "siddhirs2003@gmail.com",
	classifiers = [
		"Framework :: Django",
		"Programming Language :: Python :: 3",
	],
)