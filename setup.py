from distutils.core import setup

packages = \
['importlib_resources',
 'importlib_resources.tests',
 'importlib_resources.tests.data01',
 'importlib_resources.tests.data01.subdirectory',
 'importlib_resources.tests.data02',
 'importlib_resources.tests.data02.one',
 'importlib_resources.tests.data02.two',
 'importlib_resources.tests.data03',
 'importlib_resources.tests.data03.namespace.portion1',
 'importlib_resources.tests.data03.namespace.portion2',
 'importlib_resources.tests.zipdata01',
 'importlib_resources.tests.zipdata02']

package_data = \
{'': ['*'],
 'importlib_resources': ['docs/*', 'docs/_static/*'],
 'importlib_resources.tests.data03': ['namespace/*']}

extras_require = \
{":python_version < '3'": ['pathlib2'], ":python_version < '3.5'": ['typing']}

setup(name='importlib_resources',
      version='0.5',
      description='Read resources contained within a package.',
      author='Barry Warsaw',
      author_email='barry@python.org',
      url='http://importlib-resources.readthedocs.io/',
      packages=packages,
      package_data=package_data,
      extras_require=extras_require,
      python_requires='>=2.7,!=3.0,!=3.1,!=3.2,!=3.3',
     )
