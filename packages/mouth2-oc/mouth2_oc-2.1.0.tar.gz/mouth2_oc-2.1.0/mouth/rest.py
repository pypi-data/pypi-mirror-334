# coding=utf8
""" Mouth REST

Handles starting the REST server using the Mouth service
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

# Module imports
from mouth.service import Mouth

def errors(error):

	# If we don't send out errors
	if not config.mouth.send_error_emails(False):
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

	# Add the global prepend
	Record_MySQL.db_prepend(config.mysql.prepend(''))

	# Add the primary mysql DB
	Record_MySQL.add_host(
		'mouth',
		config.mysql.hosts[config.mouth.mysql('primary')]({
			'host': 'localhost',
			'port': 3306,
			'charset': 'utf8mb4',
			'user': 'root',
			'passwd': ''
		})
	)

	# Init the service
	oMouth = Mouth()

	# Register the services
	oRest = register_services({ 'mouth': oMouth })

	# Get config
	dMouth = oRest['mouth']

	# Create the REST server using the Client instance
	oServer = REST(
		name = 'mouth',
		instance = oMouth,
		cors = config.body.rest.allowed('mouth.local'),
		on_errors = errors,
		verbose = config.mouth.verbose(False)
	)

	# Run the REST server
	oServer.run(
		host = dMouth['host'],
		port = dMouth['port'],
		workers = dMouth['workers'],
		timeout = 'timeout' in dMouth and \
			dMouth['timeout'] or 30
	)