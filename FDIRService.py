"""
FILE_NAME:			FDIRService.py

AUTHOR:				Keenan Burnett

PURPOSE:			This class shall house the FDIR service and all related methods.

FILE REFERENCES:

LIBRARIES USED:		os, multiprocessing

SUPERCLASS:			PUSService

ABNORMAL TERMINATION CONDITIONS, ERROR AND WARNING MESSAGES: None yet.

ASSUMPTIONS, CONSTRAINTS, CONDITIONS: None.

NOTES:
					...
REQUIREMENTS:

DEVELOPMENT HISTORY:

11/17/2015			Created.

"""

import os
from multiprocessing import *
import PUSService

class FDIRService(PUSService):
	"""
	This class is meant to represent the PUS FDIR Service.
	"""
	@classmethod
	def run(self):
	"""
	@purpose:   Used to house the main program for the fdir service.
	@Note:		Since this class is a subclass of Process, when self.start() is executed on an 
				instance of this class, a process will be created with the contents of run() as the 
				main program.
	"""	


def __init__(self, path1, path2, path3, path4, path5, path6, path7, path8, tcLock, eventPath, hkPath, errorPath, eventLock, hkLock, cliLock, errorLock, day, hour, minute, second):
	# Inititalize this instance as a PUS service
	super(FDIRService, self).__init__(path1, path2, tcLock, eventPath, hkPath, errorPath, eventLock, hkLock, cliLock, errorLock, day, hour, minute, second)
	# self.processID = 0x10
	# self.serviceType = 3
	# self.currentHK[]
	# self.hkDefinition0[]
	# self.hkDefinition1[]
	# self.currentHKDefinition[]
	# self.currenthkdefinitionf = 0
	# self.collectionInterval0 = 30	# Housekeeping colleciton interval in minutes.
	# self.collectionInterval1 = 30
	# self.numParameters0 = 41
	# self.numSensors0 = 27
	# self.numVars0 = 14
	# self.numParameters1 = 41
	# self.numSensors1 = 27
	# self.numVars1 = 14

	# FIFOs for communication with the FDIR service
	self.hktoFDIRFifo 		= open(path3, "rb")
	self.memtoFDIRFifo 		= open(path4, "rb")
	self.schedtoFDIRFifo 	= open(path5, "rb")
	self.FDIRtohkFifo		= open(path6, "wb")
	self.FDIRtomemFifo		= open(path7, "wb")
	self.FDIRtoschedFifo	= open(path8, "wb")

if __name__ == '__main__':
	return
	