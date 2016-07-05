#
#  ANC350lib is a Python implementation of the C++ header provided
#     with the attocube ANC350 closed-loop positioner system.
#
#  It depends on anc350v4.dll and libusb0.dll, which are provided by attocube in the
#     ANC350_Library folder on the driver disc. Place all
#     of these in the same folder as this module (and that of ANC350lib).
#     This should also work with anc350v3.dll, although this has not been thoroughly checked.
#
#                ANC350lib is written by Rob Heath
#                      rob@robheath.me.uk
#                         24-Feb-2015
#                       robheath.me.uk
#
#                 ANC350v4lib by Brian Schaefer
#                      bts72@cornell.edu
#                         5-Jul-2016
#              http://nowack.lassp.cornell.edu/


import ctypes, os, time

#
# List of error types
#
ANC_Ok = 0 #                    No error
ANC_Error = -1 #                Unknown / other error
ANC_Timeout = 1 #               Timeout during data retrieval
ANC_NotConnected = 2 #          No contact with the positioner via USB
ANC_DriverError = 3 #           Error in the driver response
ANC_DeviceLocked = 7 #          A connection attempt failed because the device is already in use
ANC_Unknown = 8 # Unknown error.
ANC_NoDevice = 9 # Invalid device number used in call
ANC_NoAxis = 10 # Invalid axis number in function call
ANC_OutOfRange = 11 # Parameter in call is out of range
ANC_NotAvailable = 12 # Function not available for device type

#checks the errors returned from the dll
def checkError(code,func,args):
    if code == ANC_Ok:
        return
    elif code == ANC_Error:             
        raise Exception("Error: unspecific in"+str(func.__name__)+"with parameters:"+str(args))
    elif code == ANC_Timeout:           
        raise Exception("Error: comm. timeout in"+str(func.__name__)+"with parameters:"+str(args))
    elif code == ANC_NotConnected:      
        raise Exception("Error: not connected") 
    elif code == ANC_DriverError:       
        raise Exception("Error: driver error") 
    elif code == ANC_DeviceLocked:      
        raise Exception("Error: device locked")
    elif code == ANC_NoDevice:
        raise Exception("Error: invalid device number")
    elif code == ANC_NoAxis:
        raise Exception("Error: invalid axis number")
    elif code == ANC_OutOfRange:
        raise Exception("Error: parameter out of range")
    elif code == ANC_NotAvailable:
        raise Exception("Error: function not available")
    else:                    
        raise Exception("Error: unknown in"+str(func.__name__)+"with parameters:"+str(args))
    return code

# import dll - have to change directories so it finds libusb0.dll
directory_of_this_module_and_dlls = os.path.dirname(os.path.realpath(__file__))
current_directory = os.getcwd()
os.chdir(directory_of_this_module_and_dlls)
anc350v4 = ctypes.windll.LoadLibrary(directory_of_this_module_and_dlls+'\\anc350v3.dll')
os.chdir(current_directory)

#aliases for the strangely-named functions from the dll
discover = getattr(anc350v4,"ANC_discover")
getDeviceInfo = getattr(anc350v4,"ANC_getDeviceInfo")
connect = getattr(anc350v4,"ANC_connect")
disconnect = getattr(anc350v4,"ANC_disconnect")
getDeviceConfig = getattr(anc350v4,"ANC_getDeviceConfig")
getAxisStatus = getattr(anc350v4,"ANC_getAxisStatus")
setAxisOutput = getattr(anc350v4,"ANC_setAxisOutput")
setAmplitude = getattr(anc350v4,"ANC_setAmplitude")
setFrequency = getattr(anc350v4,"ANC_setFrequency")
setDcVoltage = getattr(anc350v4,"ANC_setDcVoltage")
getAmplitude = getattr(anc350v4,"ANC_getAmplitude")
getFrequency = getattr(anc350v4,"ANC_getFrequency")
startSingleStep = getattr(anc350v4,"ANC_startSingleStep")
startContinousMove = getattr(anc350v4,"ANC_startContinousMove")
startAutoMove = getattr(anc350v4,"ANC_startAutoMove")
setTargetPosition = getattr(anc350v4,"ANC_setTargetPosition")
setTargetRange = getattr(anc350v4,"ANC_setTargetRange")
getPosition = getattr(anc350v4,"ANC_getPosition")
getFirmwareVersion = getattr(anc350v4,"ANC_getFirmwareVersion")
configureExtTrigger = getattr(anc350v4,"ANC_configureExtTrigger")
configureAQuadBIn = getattr(anc350v4,"ANC_configureAQuadBIn")
configureAQuadBOut = getattr(anc350v4,"ANC_configureAQuadBOut")
configureRngTriggerPol = getattr(anc350v4,"ANC_configureRngTriggerPol")
configureRngTrigger = getattr(anc350v4,"ANC_configureRngTrigger")
configureRngTriggerEps = getattr(anc350v4,"ANC_configureRngTriggerEps")
configureNslTrigger = getattr(anc350v4,"ANC_configureNslTrigger")
configureNslTriggerAxis = getattr(anc350v4,"ANC_configureNslTriggerAxis")
selectActuator = getattr(anc350v4,"ANC_selectActuator")
getActuatorName = getattr(anc350v4,"ANC_getActuatorName")
getActuatorType = getattr(anc350v4,"ANC_getActuatorType")
measureCapacitance = getattr(anc350v4,"ANC_measureCapacitance")
saveParams = getattr(anc350v4,"ANC_saveParams")

#set error checking & handling
discover.errcheck = checkError
connect.errcheck = checkError
disconnect.errcheck = checkError
getDeviceConfig.errcheck = checkError
getAxisStatus.errcheck = checkError
setAxisOutput.errcheck = checkError
setAmplitude.errcheck = checkError
setFrequency.errcheck = checkError
setDcVoltage.errcheck = checkError
getAmplitude.errcheck = checkError
getFrequency.errcheck = checkError
startSingleStep.errcheck = checkError
startContinousMove.errcheck = checkError
startAutoMove.errcheck = checkError
setTargetPosition.errcheck = checkError
setTargetRange.errcheck = checkError
getPosition.errcheck = checkError
getFirmwareVersion.errcheck = checkError
configureExtTrigger.errcheck = checkError
configureAQuadBIn.errcheck = checkError
configureAQuadBOut.errcheck = checkError
configureRngTriggerPol.errcheck = checkError
configureRngTrigger.errcheck = checkError
configureRngTriggerEps.errcheck = checkError
configureNslTrigger.errcheck = checkError
configureNslTriggerAxis.errcheck = checkError
selectActuator.errcheck = checkError
getActuatorName.errcheck = checkError
getActuatorType.errcheck = checkError
measureCapacitance.errcheck = checkError
saveParams.errcheck = checkError
