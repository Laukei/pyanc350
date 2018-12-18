import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "pyanc350",
	version = "0.9.1",
	author = "Robert Heath",
	author_email = "rob@robheath.me.uk",
	description = "Windows wrapper for attocube systems AG's ANC350 control DLL",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/Laukei/attocube-ANC350-Python-library",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: Microsoft :: Windows",
		"Development Status :: 3 - Alpha"]

	)