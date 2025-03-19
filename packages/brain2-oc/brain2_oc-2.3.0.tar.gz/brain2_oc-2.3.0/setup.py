from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='brain2_oc',
	version='2.3.0',
	description='Brain contains a service to manage users and permissions',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/body/brain2',
	project_urls={
		'Documentation': 'https://ouroboroscoding.com/body/brain2',
		'Source': 'https://github.com/ouroboroscoding/brain2',
		'Tracker': 'https://github.com/ouroboroscoding/brain2/issues'
	},
	keywords=[ 'rest', 'microservices', 'authorization', 'authentication' ],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='Custom',
	packages=[ 'brain' ],
	package_data={ 'brain': [
		'define/*.json',
		'helpers/*.py',
		'records/*.py',
		'upgrades/*.py'
	] },
	python_requires='>=3.10',
	install_requires=[
		'body-oc>=2.0.2,<2.1',
		'config-oc>=1.1.0,<1.2',
		'define-oc>=1.0.5,<1.1',
		'email-smtp>=1.0.1,<1.1',
		'google-api-python-client>=2.118.0',
		'google-auth-oauthlib>=1.2.0,<1.3',
		'jsonb>=1.0.0,<1.1',
		'namedredis>=1.0.2,<1.1',
		'rest_mysql>=1.2.0,<1.3',
		'strings-oc>=1.0.7,<1.1',
		'tools-oc>=1.2.5,<1.3',
		'undefined-oc>=1.0.0,<1.1',
		'upgrade_oc>=1.1.0,<1.2'
	],
	entry_points={
		'console_scripts': ['brain=brain.__main__:cli']
	},
	zip_safe=True
)