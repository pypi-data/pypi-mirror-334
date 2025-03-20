from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

lib_name = "NLPUtilsBERT"

setup(name=lib_name,
      version="0.0.4",
      packages=find_packages(include=[lib_name, f"{lib_name}.*"]),
      url=f"https://github.com/AeroVikas/{lib_name}.git",
      license="MIT",
      author="Vikas Goel",
      author_email="vikas.aero@gmail.com",
      maintainer="Vikas Goel",
      maintainer_email="vikas.aero@gmail.com",
      download_url=f'https://github.com/AeroVikas/{lib_name}.git',
      keywords=['Furuness', 'Login', 'login', 'terminal'],

      description="Common Utilities",
      long_description=long_description,
      long_description_content_type="text/markdown",
      scripts=[],
      install_requires=requirements,
      project_urls={"Bug Tracker": "https://github.com/pypa/sampleproject/issues", },
      python_requires=">=3.11.9",

      include_package_data=True,
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'], )
