# coding=utf-8

from setuptools import setup, find_packages
import os

version = '0.5.1'

setup(name='upfront.simplereferencefield',
      version=version,
      description="Store references on an object and not in the reference catalog",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Zope2",
        "Framework :: Plone",
        ],
      keywords='',
      author='Roché Compaan',
      author_email='roche@upfrontsystems.co.za',
      url='http://svn.plone.org/svn/collective/upfront.simplereferencefield',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upfront'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
