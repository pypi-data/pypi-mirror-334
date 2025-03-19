# coding=utf8
""" Install

Method to install the necessary brain tables
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-07-12"

# Ouroboros imports
from config import config
from upgrade_oc import set_latest
from rest_mysql import Record_MySQL

# Python imports
from os.path import abspath, expanduser
from pathlib import Path

# Module imports
from brain.helpers import access
from brain.records import key, permission, user

def run() -> int:
	"""Run

	Entry point into the install process. Will install required files, tables, \
	records, etc. for the service

	Returns:
		int
	"""

	# Add the global prepend
	Record_MySQL.db_prepend(config.mysql.prepend(''))

	# Add the primary mysql DB
	Record_MySQL.add_host(
		'brain',
		config.mysql.hosts[config.brain.mysql('primary')]({
			'host': 'localhost',
			'port': 3306,
			'charset': 'utf8mb4',
			'user': 'root',
			'passwd': ''
		})
	)

	# Install tables
	key.Key.table_create()
	permission.Permission.table_create()
	user.User.table_create()

	# If we don't have an admin
	if not user.User.filter(
		{ 'email': 'admin@localhost' },
		raw = '_id',
		limit = 1
	):

		# Install admin
		oUser = user.User({
			'email': 'admin@localhost',
			'passwd': user.User.password_hash('Admin123'),
			'locale': config.brain.user_default_locale('en-US'),
			'first_name': 'Admin',
			'last_name': 'Istrator'
		})
		sUserId = oUser.create(changes = { 'user': access.SYSTEM_USER_ID })

		# Add admin permissions
		permission.Permission.create_many([
			permission.Permission({
				'_user': sUserId,
				'_portal': '',
				'name': 'brain_user',
				'id': access.RIGHTS_ALL_ID,
				'rights': access.C | access.R | access.U
			}),
			permission.Permission({
				'_user': sUserId,
				'_portal': '',
				'name': 'brain_permission',
				'id': access.RIGHTS_ALL_ID,
				'rights': access.R | access.U
			})
		])

	# Get the path to the data folder
	sData = config.brain.data('./.data')
	if '~' in sData:
		sData = expanduser(sData)
	sData = abspath(sData)

	# Store the last known upgrade version
	set_latest(
		sData,
		Path(__file__).parent.resolve()
	)

	# Return OK
	return 0