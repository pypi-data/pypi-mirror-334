from setuptools import setup

setup(name='http-server-pytest-fixtures',
      author='Mark Watts',
      author_email='mark@openworm.org',
      version='0.0.2',
      install_requires=['requests', 'pytest'],
      url='https://github.com/mwatts15/http-server-pytest-fixtures',
      entry_points={'pytest11': [
          'http_server = http_server_pytest_fixtures.fixtures']},
      package_data={'http_server_pytest_fixtures': ['gencert.sh']},
      packages=['http_server_pytest_fixtures'],
      classifiers=["Framework :: Pytest"])
