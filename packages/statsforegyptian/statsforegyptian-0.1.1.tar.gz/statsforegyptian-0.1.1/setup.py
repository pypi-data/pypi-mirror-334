from setuptools import setup, find_packages
with open('README.md') as file:
    description = file.read()

setup(author= "Mohamed Habashy Hussein", 
      discription= "statsforegyptian model for Item Response Theory",
      name= "statsforegyptian",
      version="0.1.1",
      packages=find_packages(include=['statsforegyptian', 'statsforegyptian.*']),
      install_requires=[],
)
