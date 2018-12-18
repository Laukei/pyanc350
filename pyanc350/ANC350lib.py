#
#  ANC350lib is a Python implementation of the C++ header provided
#     with the attocube ANC350 closed-loop positioner system.
#
#  It depends on anc350v2.dll which is provided by attocube in the
#     ANC350_DLL folders on the driver disc.
#     This in turn requires nhconnect.dll and libusb0.dll. Place all
#     of these in the same folder as this module (and that of ANC350lib).
#
#                ANC350lib is written by Rob Heath
#                      rob@robheath.me.uk
#                         24-Feb-2015
#                       robheath.me.uk
#
#    v1.1: corrected POINTER used in intEnable (!!)
#


import ctypes
import time
#
# List of error types
#

NCB_Ok = 0 #                    No error
NCB_Error = -1 #                Unknown / other error
NCB_Timeout = 1 #               Timeout during data retrieval
NCB_NotConnected = 2 #          No contact with the positioner via USB
NCB_DriverError = 3 #           Error in the driver response
NCB_BootIgnored	= 4 #           Ignored boot, equipment was already running
NCB_FileNotFound = 5 #          Boot image not found
NCB_InvalidParam = 6 #          Transferred parameter is invalid
NCB_DeviceLocked = 7 #          A connection attempt failed because the device is already in use
NCB_NotSpecifiedParam = 8 #     Transferred parameter is out of specification


#checks the errors returned from the dll
def checkError(code,func,args):
	if code == NCB_Ok:
		return
	elif code == NCB_BootIgnored:	   
		print("Warning: boot ignored in",func.__name__,"with parameters:",args)
		return
	elif code == NCB_Error:			 
		raise Exception("Error: unspecific in"+str(func.__name__)+"with parameters:"+str(args))
	elif code == NCB_Timeout:		   
		raise Exception("Error: comm. timeout in"+str(func.__name__)+"with parameters:"+str(args))
	elif code == NCB_NotConnected:	  
		raise Exception("Error: not connected") 
	elif code == NCB_DriverError:	   
		raise Exception("Error: driver error") 
	elif code == NCB_FileNotFound:	  
		raise Exception("Error: file not found") 
	elif code == NCB_InvalidParam:	  
		raise Exception("Error: invalid parameter")
	elif code == NCB_DeviceLocked:	  
		raise Exception("Error: device locked")
	elif code == NCB_NotSpecifiedParam: 
		raise Exception("Error: unspec. parameter in"+str(func.__name__)+"with parameters:"+str(args))
	else:					
		raise Exception("Error: unknown in"+str(func.__name__)+"with parameters:"+str(args))
	return code

#import dll
anc350v2 = ctypes.windll.anc350v2

#creates alias for c_int as "Int32" (I really don't know why)
Int32 = ctypes.c_int

#structure for PositionerInfo to handle positionerCheck return data
class PositionerInfo(ctypes.Structure):
	_fields_ = [("id",Int32),
				("locked",ctypes.c_bool)]

#aliases for the strangely-named functions from the dll
positionerAcInEnable = getattr(anc350v2,"_PositionerAcInEnable@12")
positionerAmplitude = getattr(anc350v2,"_PositionerAmplitude@12")
positionerAmplitudeControl = getattr(anc350v2,"_PositionerAmplitudeControl@12")
positionerBandwidthLimitEnable = getattr(anc350v2,"_PositionerBandwidthLimitEnable@12")
positionerCapMeasure = getattr(anc350v2,"_PositionerCapMeasure@12")
positionerCheck = getattr(anc350v2,"_PositionerCheck@4")
positionerClearStopDetection = getattr(anc350v2,"_PositionerClearStopDetection@8")
positionerClose = getattr(anc350v2,"_PositionerClose@4")
positionerConnect = getattr(anc350v2,"_PositionerConnect@8")
positionerDcInEnable = getattr(anc350v2,"_PositionerDcInEnable@12")
positionerDCLevel = getattr(anc350v2,"_PositionerDCLevel@12")
positionerDutyCycleEnable = getattr(anc350v2,"_PositionerDutyCycleEnable@8")
positionerDutyCycleOffTime = getattr(anc350v2,"_PositionerDutyCycleOffTime@8")
positionerDutyCyclePeriod = getattr(anc350v2,"_PositionerDutyCyclePeriod@8")
positionerExternalStepBkwInput = getattr(anc350v2,"_PositionerExternalStepBkwInput@12")
positionerExternalStepFwdInput = getattr(anc350v2,"_PositionerExternalStepFwdInput@12")
positionerExternalStepInputEdge = getattr(anc350v2,"_PositionerExternalStepInputEdge@12")
positionerFrequency = getattr(anc350v2,"_PositionerFrequency@12")
positionerGetAcInEnable = getattr(anc350v2,"_PositionerGetAcInEnable@12")
positionerGetAmplitude = getattr(anc350v2,"_PositionerGetAmplitude@12")
positionerGetBandwidthLimitEnable = getattr(anc350v2,"_PositionerGetBandwidthLimitEnable@12")
positionerGetDcInEnable = getattr(anc350v2,"_PositionerGetDcInEnable@12")
positionerGetDcLevel = getattr(anc350v2,"_PositionerGetDcLevel@12")
positionerGetFrequency = getattr(anc350v2,"_PositionerGetFrequency@12")
positionerGetIntEnable = getattr(anc350v2,"_PositionerGetIntEnable@12")
positionerGetPosition = getattr(anc350v2,"_PositionerGetPosition@12")
positionerGetReference = getattr(anc350v2,"_PositionerGetReference@16")
positionerGetReferenceRotCount = getattr(anc350v2,"_PositionerGetReferenceRotCount@12")
positionerGetRotCount = getattr(anc350v2,"_PositionerGetRotCount@12")
positionerGetSpeed = getattr(anc350v2,"_PositionerGetSpeed@12")
positionerGetStatus = getattr(anc350v2,"_PositionerGetStatus@12")
positionerGetStepwidth = getattr(anc350v2,"_PositionerGetStepwidth@12")
positionerIntEnable = getattr(anc350v2,"_PositionerIntEnable@12")
positionerLoad = getattr(anc350v2,"_PositionerLoad@12")
positionerMoveAbsolute = getattr(anc350v2,"_PositionerMoveAbsolute@16")
positionerMoveAbsoluteSync = getattr(anc350v2,"_PositionerMoveAbsoluteSync@8")
positionerMoveContinuous = getattr(anc350v2,"_PositionerMoveContinuous@12")
positionerMoveReference = getattr(anc350v2,"_PositionerMoveReference@8")
positionerMoveRelative = getattr(anc350v2,"_PositionerMoveRelative@16")
positionerMoveSingleStep = getattr(anc350v2,"_PositionerMoveSingleStep@12")
positionerQuadratureAxis = getattr(anc350v2,"_PositionerQuadratureAxis@12")
positionerQuadratureInputPeriod = getattr(anc350v2,"_PositionerQuadratureInputPeriod@12")
positionerQuadratureOutputPeriod = getattr(anc350v2,"_PositionerQuadratureOutputPeriod@12")
positionerResetPosition = getattr(anc350v2,"_PositionerResetPosition@8")
positionerSensorPowerGroupA = getattr(anc350v2,"_PositionerSensorPowerGroupA@8")
positionerSensorPowerGroupB = getattr(anc350v2,"_PositionerSensorPowerGroupB@8")
positionerSetHardwareId = getattr(anc350v2,"_PositionerSetHardwareId@8")
positionerSetOutput = getattr(anc350v2,"_PositionerSetOutput@12")
positionerSetStopDetectionSticky = getattr(anc350v2,"_PositionerSetStopDetectionSticky@12")
positionerSetTargetGround = getattr(anc350v2,"_PositionerSetTargetGround@12")
positionerSetTargetPos = getattr(anc350v2,"_PositionerSetTargetPos@16")
positionerSingleCircleMode = getattr(anc350v2,"_PositionerSingleCircleMode@12")
positionerStaticAmplitude = getattr(anc350v2,"_PositionerStaticAmplitude@8")
positionerStepCount = getattr(anc350v2,"_PositionerStepCount@12")
positionerStopApproach = getattr(anc350v2,"_PositionerStopApproach@8")
positionerStopDetection = getattr(anc350v2,"_PositionerStopDetection@12")
positionerStopMoving = getattr(anc350v2,"_PositionerStopMoving@8")
positionerTrigger = getattr(anc350v2,"_PositionerTrigger@16")
positionerTriggerAxis = getattr(anc350v2,"_PositionerTriggerAxis@12")
positionerTriggerEpsilon = getattr(anc350v2,"_PositionerTriggerEpsilon@12")
positionerTriggerModeIn = getattr(anc350v2,"_PositionerTriggerModeIn@8")
positionerTriggerModeOut = getattr(anc350v2,"_PositionerTriggerModeOut@8")
positionerTriggerPolarity = getattr(anc350v2,"_PositionerTriggerPolarity@12")
positionerUpdateAbsolute = getattr(anc350v2,"_PositionerUpdateAbsolute@12")

#set error checking & handling
positionerAcInEnable.errcheck = checkError
positionerAmplitude.errcheck = checkError
positionerAmplitudeControl.errcheck = checkError
positionerBandwidthLimitEnable.errcheck = checkError
positionerCapMeasure.errcheck = checkError
positionerClearStopDetection.errcheck = checkError
positionerClose.errcheck = checkError
positionerConnect.errcheck = checkError
positionerDcInEnable.errcheck = checkError
positionerDCLevel.errcheck = checkError
positionerDutyCycleEnable.errcheck = checkError
positionerDutyCycleOffTime.errcheck = checkError
positionerDutyCyclePeriod.errcheck = checkError
positionerExternalStepBkwInput.errcheck = checkError
positionerExternalStepFwdInput.errcheck = checkError
positionerExternalStepInputEdge.errcheck = checkError
positionerFrequency.errcheck = checkError
positionerGetAcInEnable.errcheck = checkError
positionerGetAmplitude.errcheck = checkError
positionerGetBandwidthLimitEnable.errcheck = checkError
positionerGetDcInEnable.errcheck = checkError
positionerGetDcLevel.errcheck = checkError
positionerGetFrequency.errcheck = checkError
positionerGetIntEnable.errcheck = checkError
positionerGetPosition.errcheck = checkError
positionerGetReference.errcheck = checkError
positionerGetReferenceRotCount.errcheck = checkError
positionerGetRotCount.errcheck = checkError
positionerGetSpeed.errcheck = checkError
positionerGetStatus.errcheck = checkError
positionerGetStepwidth.errcheck = checkError
positionerIntEnable.errcheck = checkError
positionerLoad.errcheck = checkError
positionerMoveAbsolute.errcheck = checkError
positionerMoveAbsoluteSync.errcheck = checkError
positionerMoveContinuous.errcheck = checkError
positionerMoveReference.errcheck = checkError
positionerMoveRelative.errcheck = checkError
positionerMoveSingleStep.errcheck = checkError
positionerQuadratureAxis.errcheck = checkError
positionerQuadratureInputPeriod.errcheck = checkError
positionerQuadratureOutputPeriod.errcheck = checkError
positionerResetPosition.errcheck = checkError
positionerSensorPowerGroupA.errcheck = checkError
positionerSensorPowerGroupB.errcheck = checkError
positionerSetHardwareId.errcheck = checkError
positionerSetOutput.errcheck = checkError
positionerSetStopDetectionSticky.errcheck = checkError
positionerSetTargetGround.errcheck = checkError
positionerSetTargetPos.errcheck = checkError
positionerSingleCircleMode.errcheck = checkError
positionerStaticAmplitude.errcheck = checkError
positionerStepCount.errcheck = checkError
positionerStopApproach.errcheck = checkError
positionerStopDetection.errcheck = checkError
positionerStopMoving.errcheck = checkError
positionerTrigger.errcheck = checkError
positionerTriggerAxis.errcheck = checkError
positionerTriggerEpsilon.errcheck = checkError
positionerTriggerModeIn.errcheck = checkError
positionerTriggerModeOut.errcheck = checkError
positionerTriggerPolarity.errcheck = checkError
positionerUpdateAbsolute.errcheck = checkError
#positionerCheck.errcheck = checkError
#positionerCheck returns number of attached devices; gives "comms error" if this is applied, despite working fine

#set argtypes
positionerAcInEnable.argtypes = [Int32, Int32, ctypes.c_bool]
positionerAmplitude.argtypes = [Int32, Int32, Int32]
positionerAmplitudeControl.argtypes = [Int32, Int32, Int32]
positionerBandwidthLimitEnable.argtypes = [Int32, Int32, ctypes.c_bool]
positionerCapMeasure.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerCheck.argtypes = [ctypes.POINTER(PositionerInfo)]
positionerClearStopDetection.argtypes = [Int32, Int32]
positionerClose.argtypes = [Int32]
positionerConnect.argtypes = [Int32, ctypes.POINTER(Int32)]
positionerDcInEnable.argtypes = [Int32, Int32, ctypes.c_bool]
positionerDCLevel.argtypes = [Int32, Int32, Int32]
positionerDutyCycleEnable.argtypes = [Int32, ctypes.c_bool]
positionerDutyCycleOffTime.argtypes = [Int32, Int32]
positionerDutyCyclePeriod.argtypes = [Int32, Int32]
positionerExternalStepBkwInput.argtypes = [Int32, Int32, Int32]
positionerExternalStepFwdInput.argtypes = [Int32, Int32, Int32]
positionerExternalStepInputEdge.argtypes = [Int32, Int32, Int32]
positionerFrequency.argtypes = [Int32, Int32, Int32]
positionerGetAcInEnable.argtypes = [Int32, Int32, ctypes.POINTER(ctypes.c_bool)]
positionerGetAmplitude.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerGetBandwidthLimitEnable.argtypes = [Int32, Int32, ctypes.POINTER(ctypes.c_bool)]
positionerGetDcInEnable.argtypes = [Int32, Int32, ctypes.POINTER(ctypes.c_bool)]
positionerGetDcLevel.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerGetFrequency.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerGetIntEnable.argtypes = [Int32, Int32, ctypes.POINTER(ctypes.c_bool)]
positionerGetPosition.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerGetReference.argtypes = [Int32, Int32, ctypes.POINTER(Int32), ctypes.POINTER(ctypes.c_bool)]
positionerGetReferenceRotCount.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerGetRotCount.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerGetSpeed.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerGetStatus.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerGetStepwidth.argtypes = [Int32, Int32, ctypes.POINTER(Int32)]
positionerIntEnable.argtypes = [Int32, Int32, ctypes.c_bool]
positionerLoad.argtypes = [Int32, Int32, ctypes.POINTER(ctypes.c_char)]
positionerMoveAbsolute.argtypes = [Int32, Int32, Int32, Int32]
positionerMoveAbsoluteSync.argtypes = [Int32, Int32]
positionerMoveContinuous.argtypes = [Int32, Int32, Int32]
positionerMoveReference.argtypes = [Int32, Int32]
positionerMoveRelative.argtypes = [Int32, Int32, Int32, Int32]
positionerMoveSingleStep.argtypes = [Int32, Int32, Int32]
positionerQuadratureAxis.argtypes = [Int32, Int32, Int32]
positionerQuadratureInputPeriod.argtypes = [Int32, Int32, Int32]
positionerQuadratureOutputPeriod.argtypes = [Int32, Int32, Int32]
positionerResetPosition.argtypes = [Int32, Int32]
positionerSensorPowerGroupA.argtypes = [Int32, ctypes.c_bool]
positionerSensorPowerGroupB.argtypes = [Int32, ctypes.c_bool]
positionerSetHardwareId.argtypes = [Int32, Int32]
positionerSetOutput.argtypes = [Int32, Int32, ctypes.c_bool]
positionerSetStopDetectionSticky.argtypes = [Int32, Int32, ctypes.c_bool]
positionerSetTargetGround.argtypes = [Int32, Int32, ctypes.c_bool]
positionerSetTargetPos.argtypes = [Int32, Int32, Int32, Int32]
positionerSingleCircleMode.argtypes = [Int32, Int32, ctypes.c_bool]
positionerStaticAmplitude.argtypes = [Int32, Int32]
positionerStepCount.argtypes = [Int32, Int32, Int32]
positionerStopApproach.argtypes = [Int32, Int32]
positionerStopDetection.argtypes = [Int32, Int32, ctypes.c_bool]
positionerStopMoving.argtypes = [Int32, Int32]
positionerTrigger.argtypes = [Int32, Int32, Int32, Int32]
positionerTriggerAxis.argtypes = [Int32, Int32, Int32]
positionerTriggerEpsilon.argtypes = [Int32,Int32, Int32]
positionerTriggerModeIn.argtypes = [Int32, Int32]
positionerTriggerModeOut.argtypes = [Int32, Int32]
positionerTriggerPolarity.argtypes = [Int32, Int32, Int32]
positionerUpdateAbsolute.argtypes = [Int32, Int32, Int32]
