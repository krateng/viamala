VERBOSE_LOGGING = False

import random
import os

def logv(string):
	if VERBOSE_LOGGING:
		print(string)
def log(string):
	print(string)


def createSettingsFile():

	if not os.path.isfile("settings.ini"):
		log("Settings file not found, creating!")
		open('settings.ini',"w+").close()
