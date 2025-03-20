from setuptools import setup, find_packages
import json
import os

def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='django_server_testing',
  version='4.0.5',
  include_package_data=True,
  author='SODT',
  author_email='svsharygin@icloud.com',
  description='',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/lum0vi/django_server_testing',
  packages=find_packages( include=['django_server_testing', 'django_server_testing.*']),
  package_data={"django_server_testing" : ["nto/*", "temp_files/nto/launcher/*.exe", "temp_files/nto/launcher/*.nasm",
  "temp_files/nto/launcher/*.o", "temp_files/nto/templates/*.html", "temp_files/nto/templates/TODO/*.html",
  "temp_files/nto/staticfiles/js/*.js", "temp_files/nto/staticfiles/css/*.css", "temp_files/nto/staticfiles/img/*.svg",
  "temp_files/nto/staticfiles/img/*.svg", "temp_files/nto/nto/__pycache__/*.pyc", "temp_files/nto/mainapp/__pycache__/*.pyc",
  "temp_files/nto/mainapp/templatetags/__pycache__/*.pyc", "temp_files/nto/mainapp/migrations/__pycache__/*.pyc",
  "test_server/update_tests/*.data"]
  },
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
  ],
  keywords='files speedfiles',
  project_urls={
    'GitHub': 'https://github.com/lum0vi/django_server_testing'
  },
  python_requires='>=3.6'
)
