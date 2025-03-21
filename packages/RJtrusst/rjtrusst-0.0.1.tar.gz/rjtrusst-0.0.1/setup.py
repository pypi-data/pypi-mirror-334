from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='RJtrusst',
  version='0.0.1',
  description='testing a library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Raghav Agarwal',
  author_email='raghav.mje@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='testing', 
  packages=find_packages(),
  install_requires=[''] 
)