from setuptools import setup, find_packages

setup(name='hhtrade',
      version='3.1',
packages=find_packages(),
	  install_requires=[
      'tqsdk==3.7.6',
		  'requests == 2.28.1',
		  'texttable == 1.7.0'
	  ],
	  author="hh",
	  author_email="hehuang0717@outlook.com",
	  description="sqllib",
	  long_description=open('README.md').read(),
	  long_description_content_type="text/markdown",
	  url="https://your.project.url",
	  classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
				   "Operating System :: OS Independent", ],
	  python_requires='>=3.9')