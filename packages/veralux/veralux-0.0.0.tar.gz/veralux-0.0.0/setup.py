from setuptools import setup, find_packages
from pathlib import Path

with open(Path(__file__).parent / "readme.md", "r", encoding="utf-8") as fh:
    long_desc = fh.read()

desc = "Effortlessly build, extend, and deploy sophisticated language-model-based agents"

setup(name='veralux',version='0.0.0',
      packages=find_packages(where="src"),
      package_dir={'': 'src'},
      install_requires=['openai'],
      include_package_data=True,
      description=desc,
      long_description=long_desc,
      long_description_content_type="text/markdown",
      author='Brent Carpenetti',
      author_email='brentcarpenetti@gmail.com',    
      license='MIT',)