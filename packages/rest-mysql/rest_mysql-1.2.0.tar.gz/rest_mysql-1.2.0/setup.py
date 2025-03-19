from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='rest_mysql',
	version='1.2.0',
	description='Stand alone version of Record_MySQL from Rest-OC to facilitate updating code to newer librairies. Has since been updated far beyond Rest-OC.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/rest_mysql',
		'Tracker': 'https://github.com/ouroboroscoding/rest_mysql/issues'
	},
	keywords=['rest','mysql','sql'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['rest_mysql'],
	python_requires='>=3.10',
	install_requires=[
		'arrow>=1.3.0,<1.4',
		'define-oc>=1.0.5,<1.1',
		'json-fix>=1.0.0,<1.1',
		'jsonb>=1.0.0,<1.1',
		'PyMySQL>=1.0.2,<1.1',
		'tools-oc>=1.2.5,<1.3'
	],
	zip_safe=True
)