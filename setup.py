from setuptools import setup


setup(name='tspy',
      version='0.1',
      description='tspy',
      url='http://github.com/peter-woyzbun/',
      author='Peter Woyzbun',
      author_email='peter.woyzbun@gmail.com',
      packages=['tspy'],
      install_requires=['pandas', 'numpy', 'matplotlib', 'tabulate', 'scipy', 'dateutil'],
      zip_safe=False)