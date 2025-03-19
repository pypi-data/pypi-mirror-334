from setuptools import setup

# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ['requests']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ]

# calling the setup function 
setup(name='vrv_mygmap',
      version='1.0.7',
      description='A small wrapper around google maps api',
      long_description=long_description,
      url='https://github.com/nikhilkumarsingh/mygmap',
      author='zoneh',
      author_email='oldmonk.h@gmail.com',
      license='MIT',
      packages=['geo'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='maps location address'
      )
