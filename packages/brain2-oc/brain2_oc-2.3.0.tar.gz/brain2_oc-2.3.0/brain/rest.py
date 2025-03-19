# coding=utf8
""" Brain REST

Handles starting the REST server using the Brain service
"""

__author__		= "Chris Nasr"
__version__		= "1.0.0"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2022-08-25"

# Ouroboros imports
from body import register_services, REST
from config import config
import em
from rest_mysql import Record_MySQL

# Python imports
from pprint import pformat
from sys import stderr

# Pip imports
from google_auth_oauthlib.flow import Flow

# Module imports
from brain.service import Brain

# Global
_ogFlow = None

def google_login():
	"""Google OAuth Login

	Handles request to show the google login using oauth

	Returns
		str
	"""

	# Pull in the flow variable
	global _ogFlow

	# If we have no flow
	if not _ogFlow:
		return REST.bottle.abort(401, 'Google OAuth not initialised')

	# Get the auth url from google
	sAuthURL, _ = _ogFlow.authorization_url(
		prompt = 'consent'
	)

	# Redirect the user to the login
	return REST.bottle.redirect(sAuthURL)

def errors(error):

	# If we don't send out errors
	if not config.brain.send_error_emails(False):
		return True

	# Generate a list of the individual parts of the error
	lErrors = [
		'ERROR MESSAGE\n\n%s\n' % error['traceback'],
		'REQUEST\n\n%s %s:%s\n' % (
			error['method'], error['service'], error['path']
		)
	]
	if 'data' in error and error['data']:
		lErrors.append('DATA\n\n%s\n' % pformat(error['data']))
	if 'session' in error and error['session']:
		lErrors.append('SESSION\n\n%s\n' % pformat({
			k:error['session'][k] for k in error['session']
		}))
	if 'environment' in error and error['environment']:
		lErrors.append('ENVIRONMENT\n\n%s\n' % pformat(error['environment']))

	# Send the email
	return em.error('\n'.join(lErrors))

def run():
	"""Run

	Starts the http REST server

	Returns:
		None
	"""

	# Pull in Flow instance
	global _ogFlow

	# Add the global prepend
	Record_MySQL.db_prepend(config.mysql.prepend(''))

	# Add the primary mysql DB
	Record_MySQL.add_host(
		'brain',
		config.mysql.hosts[config.mouth.mysql('primary')]({
			'host': 'localhost',
			'port': 3306,
			'charset': 'utf8mb4',
			'user': 'root',
			'passwd': ''
		})
	)

	# If google oauth is enabled
	dGoogle = config.brain.google(False)
	if dGoogle is not False:

		# If the redirect is missing
		if 'redirect' in dGoogle and \
			isinstance(dGoogle['redirect'], str):

			# Init scopes
			lScopes = [
				'openid',
				'https://www.googleapis.com/auth/userinfo.email',
				'https://www.googleapis.com/auth/userinfo.profile'
			]

			# If we got a string
			if isinstance(dGoogle['client_secret'], str):

				# Assume the string is a client secrets file
				_ogFlow = Flow.from_client_secrets_file(
					dGoogle['client_secret'],
					scopes = lScopes,
					redirect_uri = dGoogle['redirect']
				)

			# Else if we got a config
			elif isinstance(dGoogle['client_secret'], dict):

				# Assume the dict is a client config
				_ogFlow = Flow.from_client_config(
					dGoogle['client_secret'],
					scopes = lScopes,
					redirect_uri = dGoogle['redirect']
				)

			# Else
			else:
				print(
					'brain.google.client_secret must be str (filename) ' \
					'or dict (config)',
					file = stderr
				)

		# Else
		else:
			print('brain.google.redirect must be str', file = stderr)

	# Init the service
	oBrain = Brain(_ogFlow)

	# Register the services
	oRest = register_services({ 'brain': oBrain })

	# Get config
	dBrain = oRest['brain']

	# Create the REST server using the Client instance
	oServer = REST(
		name = 'brain',
		instance = oBrain,
		cors = config.body.rest.allowed('brain.local'),
		on_errors = errors,
		verbose = config.brain.verbose(False)
	)

	# If we have a flow
	if _ogFlow:

		# Bind the google login uri
		oServer.route('/google/login', 'GET', google_login)

	# Run the REST server
	oServer.run(
		host = dBrain['host'],
		port = dBrain['port'],
		workers = dBrain['workers'],
		timeout = 'timeout' in dBrain and \
			dBrain['timeout'] or 30
	)