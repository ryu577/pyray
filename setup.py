from setuptools import setup, find_packages

INSTALL_DEPS = ['numpy',
                'scipy',
                'matplotlib',
                'sympy',
                'pillow',
               ]
TEST_DEPS = ['pytest']
DEV_DEPS = []

setup(name='raypy',
      version='0.0.3',
      url='https://github.com/ryu577/pyray',
      license='MIT',
      author='Rohit Pandey',
      author_email='rohitpandey576@gmail.com',
      description='A 3d rendering library written completely in python.',
      packages=find_packages(exclude=['tests', 'Images', 'sounds']),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False,
      install_requires=INSTALL_DEPS,

      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',

      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[dev,test]
      extras_require={
          'dev': DEV_DEPS,
          'test': TEST_DEPS,
      },
     )
