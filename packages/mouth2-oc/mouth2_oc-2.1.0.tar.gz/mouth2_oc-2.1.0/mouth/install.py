# coding=utf8
""" Install

Method to install the necessary mouth tables
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2024-12-14"

# Ouroboros imports
from config import config
from upgrade import set_latest
from rest_mysql import Record_MySQL

# Python imports
from os.path import abspath, expanduser
from pathlib import Path

# Module imports
from mouth.records import locale, template, template_email, template_sms

def run() -> int:
	"""Run

	Entry point into the install process. Will installs required files, \
	tables, records, etc. for the service

	Returns:
		int
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

	# Install tables
	locale.Locale.table_create()
	template.Template.table_create()
	template_email.TemplateEmail.table_create()
	template_sms.TemplateSMS.table_create()

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