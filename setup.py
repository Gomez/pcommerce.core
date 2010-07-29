from setuptools import setup, find_packages
import os

version = '0.5a2'

setup(name='pcommerce.core',
      version=version,
      description="eCommerce for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone ecommerce shop',
      author='Raptus AG',
      author_email='skaeser@raptus.com',
      url='http://raptus.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pcommerce'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.SingleKeywordWidget',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
