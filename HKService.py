"""
FILE_NAME:			HKService.py

AUTHOR:				Keenan Burnett

PURPOSE:			This class shall house the housekeeping PUS service and all related methods.

FILE REFERENCES:

LIBRARIES USED:		os, multiprocessing

SUPERCLASS:			PUSService

ABNORMAL TERMINATION CONDITIONS, ERROR AND WARNING MESSAGES: None yet.

ASSUMPTIONS, CONSTRAINTS, CONDITIONS: None.

NOTES:				When parameter reports are enabled, one is automatically generated
					every time 

REQUIREMENTS:

DEVELOPMENT HISTORY:

11/17/2015			Created.

11/20/2015			Adding in the remainder of the functionality for this service.

					Other than waiting for TC Aceptance verification, I believe this
					service is mostly done now.
"""

import os
from multiprocessing import *
from PUSService import *

class hkService(PUSService):
	"""
	This class is meant to represent the PUS Housekeeping Service.
	"""
@classmethod
def run(self):
	"""
	@purpose:   Used to house the main program for the housekeeping service.
	@Note:		Since this class is a subclass of Process, when self.start() is executed on an 
				instance of this class, a process will be created with the contents of run() as the 
				main program.
	"""	
	inititalize()

	while(1):
		self.receiveCommandFromFifo(self.fifoFromGPR)		# If command in FIFO, places it in self.currentCommand[]
		execCommands()										# Deals with commands from GPR
	return				# This should never be reached.

def initialize():
	"""
	@purpose:   - Initializes arrays to 0.
				- Sets current HK definition to default.
	"""	
	tempString = None
	for i in range(0, self.dataLength):
		self.currentHK[i] = 0
		self.currentHKDefinition[i] = 0
		self.hkDefinition0[i] = 0
		self.hkDefinition1[i] = 0
	self.clearCurrentCommand()

	setHKDefinitionsDefault()
	self.logEventReport(1, self.hkgroundinitialized, 0, 0, "Ground Housekeeping Service Initialized Correctly.")
	return

def execCommands():
	"""
	@purpose:   After a command has been received in the FIFO, this function parses through it
				and performs different actions based on what is received.
	"""	
	if(self.currentCommand[146] == self.hkDefinitionReport):
		logHkParameterReport()
	if(self.currentCommand[146] == self.hkReport):
		logHKReport()
	if(self.currentCommand[146] == self.newHKDefinition):
		setAlternateHKDefinition()
	if(self.currentCommand[146] == self.clearHKDefinition):
		setHKDefinitionsDefault()
	if(self.currentCommand[146] == self.enableParamReport):
		enableParamReport()
	if(self.currentCommand[146] == self.disableParamReport):
		disableParamReport()
	if(self.currentCommand[146] == self.reportHKDefinitions):
		requestHKParamReport()
	self.clearCurrentCommand()
	return

def enableParamReport():
	self.clearCurrentCommand()
	self.currentCommand[146] = self.enableParamReport
	self.sendCurrentCommandToFifo(self.fifoToGPR)
	return

def disableParamReport():
	self.clearCurrentCommand()
	self.currentCommand[146] = self.disableParamReport
	self.sendCurrentCommandToFifo(self.fifoToGPR)
	return

def requestHKParamReport():
	self.clearCurrentCommand()
	self.currentCommand[146] = self.reportHKDefinitions
	self.sendCurrentCommandToFifo(self.fifoToGPR)
	return

def logHkParameterReport():
	"""
	@purpose:   Used to log a hk parameter report.
	@Note:		We simply use the parameter report which should be stored in currentCommand[] 
				at this point.
	"""	
	tempString = None
	sID = self.currentCommand[self.dataLength - 1]
	collectionInterval = currentCommand[145]
	numParameters = self.currentCommand[144]
	if (sID != self.currenthkdefinitionf):
		logError("Local Housekeeping Parameter definition does not match satellite")
		self.currentCommand[146] = self.hkParamIncorrect
		self.currentCommand[146] = 3
		self.sendCurrentCommandToFifo(self.fifotoFDIR)
	if (sID):
		if (collectionInterval != self.collectionInterval1):
			logError("Local HK collection Interval definition does not match satellite")
			self.currentCommand[146] = self.hkIntervalIncorrect
			self.currentCommand[146] = 3
			self.sendCurrentCommandToFifo(self.fifotoFDIR)
		if (numParameters != self.numParameters1):
			logError("Local HK number of parameters does not match satellite")
			self.currentCommand[146] = self.hkNumParamsIncorrect
			self.currentCommand[146] = 3
			self.sendCurrentCommandToFifo(self.fifotoFDIR)
	if (!sID):
		if (collectionInterval != self.collectionInterval0):
			logError("Local HK collection Interval definition does not match satellite")
			self.currentCommand[146] = self.hkIntervalIncorrect
			self.currentCommand[146] = 3
			self.sendCurrentCommandToFifo(self.fifotoFDIR)
		if (numParameters != self.numParameters0):
			logError("Local HK number of parameters does not match satellite")
			self.currentCommand[146] = self.hkNumParamsIncorrect
			self.currentCommand[146] = 3
			self.sendCurrentCommandToFifo(self.fifotoFDIR)	

	self.hkLog.write("HK PARAMETER REPORT:\t")
	self.hkLog.write(str(self.absTime.day) + "/" + str(self.absTime.day) + "/" + str(self.absTime.day) + "\t,\n")
	errorInt = 0
	for i in range(numParameters - 1, -1, -1):
		byte = self.currentCommand[i] & 0x000000FF
		tempString = self.parameters(byte)
		if !sID:
			if tempString != self.paramaters(self.hkDefinition0[i]):
				errorInt = 1
			self.hkLog.write(tempString) + "\n")
		if sID:
			if tempString != self.parameters(self.hkDefinition1[i]):
				errorInt = 1
			self.hkLog.write(tempString) + "\n")
	return

@classmethod
def logHKReport():
	"""
	@purpose:   Used to log the housekeeping report which was received.
	@Note:		Contains a mutex lock for exclusive access.
	@Note:		Housekeeping reports are created in a manner that is more convenient
				for excel or Matlab to parse but not really that great for human consumption.
	@Note:		Each parameter in a housekeeping report gets 2 entries in the array,
				which corresponds to being 16 bits on the satellite.
	@Note:		We expect housekeeping report to located in currentCommand[] at this point.
	"""	
	param = 0
	if(self.currenthkdefinitionf):
		numParameters = self.numParameters1
	else:
		numParameters = self.numParameters0

	self.hkLock.acquire()
	self.hkLog.write("HKLOG:\t")
	self.hkLog.write(str(self.absTime.day) + "/" + str(self.absTime.day) + "/" + str(self.absTime.day) + "\t,\t")
	for i in range(numParameters * 2 - 1, -1, -2)
		param = self.currentCommand[i] << 8
		param += self.currentCommand[i - 1]
		self.hkLog.write(str(param) + "\t,\t")
	self.hkLog.write("\n")
	self.hkLock.release()
	return

def setHKDefinitionsDefault():
	"""
	@purpose:   Sets the hk definition which is being used to the default.
	@Note:		For default, parameters are stored in the housekeeping definition in decreasing order for variables
				followed by increasing order for sensors (starting at hkDefinition[numParameters - 1] and descending)
	@Note:		Note: If the satellite experiences a reset, it will go back to this definition for housekeeping.
	"""	
	paramNum = 0xFF
	self.hkDefinition0[136] 	= 0
	self.hkDefinition0[135] 	= self.collectionInterval0
	self.hkDefinition0[134] 	= self.numParameters0
	for i in range(0, self.numVars0):
		self.hkDefinition0[i] = paramNum - i
		paramNum = 1
	for i in range (self.numVars0, self.numParameters0):
		self.hkDefinition0[i] = paramNum
		paramNum++
	self.currenthkdefinitionf = 0
	defPath = "/housekeeping/definitions/hkDefinition0.txt"

	# Create the hkDefinition0.txt file if it doesn't exist yet.
	if (!os.path.exists(defPath)):
		hkdef = open(defPath, "ab")
		hkdef.write(str(0))
		hkdef.write(str(self.collectionInterval0))
		hkdef.write(str(self.numParameters0))
		for i in range((self.numParameters0 * 2 - 1 ), 0, -1):
			paramNum = self.hkDefinition0[i]
			hkdef.write(self.parameters[paramNum])

	# Send a PUS Packet to the satellite setting the hk def to default (clearHKDefinition)
	self.clearCurrentCommand()
	self.currentCommand[146] = self.clearHKDefinition			
	self.sendCurrentCommandToFifo(self.fifotoFDIR)
	# Send a PUS packet to the satellite requesting a parameter report
	requestHKParamReport()
	return

def setAlternateHKDefinition():
	"""
	@purpose:   Sets the hk definition which is being used to the alternate definition.
	@Note:		The format of hk definitions should be known before changing the existing one.
	@Note:		The new housekeeping parameter report should replace hkDefinition1.txt & have an sID of 1.
	"""	
	defPath = "/housekeeping/definitions/hkDefinition1.txt"
	sID = 0
	tempString = None
	paramNum = 0
	if os.path.exists(defPath):
		hkdef = open(defPath, "rb")
		sId = int(hkdef.read(1))
		if(sID != 1):
			self.printtoCLI("sID in hkDefinition1.txt was not 1, denying definition update")
			self.logError("sID in hkDefinition1.txt was not 1, denying definition update\n")
			return
		self.hkDefinition1[136] = 1
		hkdef.seek(1)
		self.collectionInterval1 = int(hkdef.read(2))
		self.hkDefinition1[135] = self.collectionInterval1
		hkdef.seek(2)
		numParameters1 = int(hkdef.read(2))
		if(numParameters1 > 64):
			self.logError("Proposed alternate HK definition has numParameters > 64, denying definition update\n")
			return
		self.numParameters1 = numParameters1
		self.hkDefinition1[134] = self.numParameters1
		hkdef.seek(3)
		# Read the housekeeping definition from the file.
		for i in range((self.numParameters1 * 2 - 1 ), 0, -1):
			tempString = hkdef.readline()
			tempString = tempString.rstrip()
			paramNum = int(self.invParameters(tempString))
			hkDefinition1[i] = paramNum

		# Send a PUS Packet to the satellite setting the hk def to the alternate one
		self.clearCurrentCommand()
		self.currentCommand[146] = self.clearHKDefinition
		for i in range(0, self.dataLength):
			self.currentCommand[i] = self.hkDefinition1[i]
		self.sendCurrentCommandToFifo(self.fifotoFDIR)
		# Send a PUS packet to the satellite requesting a parameter report
		requestHKParamReport()
		return

	else:
		self.printtoCLI("hkDefinition1.txt does not exist, denying definition update")
		self.logError("hkDefinition1.txt does not exist, denying definition update\n")
		return

def __init__(self, path1, path2, path3, path4, tcLock, eventPath, hkPath, errorPath, eventLock, hkLock, cliLock, errorLock, day, hour, minute, second, hkDefPath):
	# Inititalize this instance as a PUS service
	super(hkService, self).__init__(path1, path2, tcLock, eventPath, hkPath, errorPath, eventLock, hkLock, cliLock, errorLock, day, hour, minute, second)
	self.processID = 0x10
	self.serviceType = 3
	self.currentHK[]
	self.hkDefinition0[]
	self.hkDefinition1[]
	self.currentHKDefinition[]
	self.currenthkdefinitionf = 0
	self.collectionInterval0 = 30	# Housekeeping colleciton interval in minutes.
	self.collectionInterval1 = 30
	self.numParameters0 = 41
	self.numSensors0 = 27
	self.numVars0 = 14
	self.numParameters1 = 41
	self.numSensors1 = 27
	self.numVars1 = 14

	# Log for Housekeeping Parameter Reports
	self.hkDefLog = open(hkDefPath, a+)

	# FIFOs for communication with the FDIR service
	self.fifotoFDIR = open(path3, "wb")
	self.fifofromFDIR = open(path4, "rb")

	# Acquire some values from the satellite.

if __name__ == '__main__':
	return