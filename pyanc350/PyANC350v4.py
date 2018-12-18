#
#  PyANC350v4 is a control scheme suitable for the Python coding style
#    for the attocube ANC350 closed-loop positioner system.
#
#  It implements ANC350v4lib, which in turn depends on anc350v4.dll and libusb0.dll, which are provided by attocube in the
#     ANC350_Library folder on the driver disc. Place all
#     of these in the same folder as this module (and that of ANC350lib).
#     This should also work with anc350v3.dll, although this has not been thoroughly checked.
#
#  Unlike ANC350v4lib which is effectively a re-imagining of the
#    C++ header, PyANC350v4 is intended to behave as one might expect
#    Python to. This means: returning values; behaving as an object.
#
#  At present this only addresses the first ANC350 connected to the
#    machine.
#
#  Usage:
#  1. instantiate Positioner() class to begin, eg. pos = Positioner().
#  2. methods from the ANC350v2 documentation are implemented such that
#      function ANC_getPosition(device, axisNo, &position)
#      becomes position = pos.getPosition(axisNo), for example. Return code handling is
#      within ANC350lib.
#  3. for tidiness remember to Positioner.close() when finished!
#
#                PyANC350 is written by Rob Heath
#                      rob@robheath.me.uk
#                         24-Feb-2015
#                       robheath.me.uk
#
#                 PyANC350v4 by Brian Schaefer
#                      bts72@cornell.edu
#                         5-Jul-2016
#              http://nowack.lassp.cornell.edu/

import ANC350v4lib as ANC
import ctypes, math

class Positioner:
    
    def __init__(self):
        self.discover()
        self.device = self.connect()
        
        
    def configureAQuadBIn(self, axisNo, enable, resolution):
        '''
        Enables and configures the A-Quad-B (quadrature) input for the target position.
        Parameters
            axisNo	Axis number (0 ... 2)
            enable	Enable (1) or disable (0) A-Quad-B input
            resolution	A-Quad-B step width in m. Internal resolution is 1 nm.
        Returns
            None
        '''
        ANC.configureAQuadBIn(self.device, axisNo, enable, ctypes.c_double(resolution))
        
        
    def configureAQuadBOut(self, axisNo, enable, resolution, clock):
        '''
        Enables and configures the A-Quad-B output of the current position.

        Parameters
            axisNo	Axis number (0 ... 2)
            enable	Enable (1) or disable (0) A-Quad-B output
            resolution	A-Quad-B step width in m; internal resolution is 1 nm
            clock	Clock of the A-Quad-B output [s]. Allowed range is 40ns ... 1.3ms; internal resulution is 20ns.
        Returns
            None
        '''
        ANC.configureAQuadBOut(self.device, axisNo, enable, ctypes.c_double(resolution), ctypes.c_double(clock))
       
    
    def configureExtTrigger(self, axisNo, mode):
        '''
        Enables the input trigger for steps.

        Parameters
            axisNo	Axis number (0 ... 2)
            mode	Disable (0), Quadratur (1), Trigger(2) for external triggering
        Returns
            None
        '''
        ANC.configureExtTrigger(self.device, axisNo, mode)
     
    
    def configureNslTrigger(self, enable):
        '''
        Enables NSL Input as Trigger Source.

        Parameters
            enable	disable(0), enable(1)
        Returns
            None
        '''
        ANC.configureNslTrigger(self.device, enable)
    
    
    def configureNslTriggerAxis(self, axisNo):
        '''
        Selects Axis for NSL Trigger.

        Parameters
            axisNo	Axis number (0 ... 2)
        Returns
            None
        '''
        ANC.configureNslTriggerAxis(self.device, axisNo)
      
    
    def configureRngTrigger(self, axisNo, lower, upper):
        '''
        Configure lower position for range Trigger.

        Parameters
            axisNo	Axis number (0 ... 2)
            lower	Lower position for range trigger (nm)
            upper	Upper position for range trigger (nm)
        Returns
            None
        '''
        ANC.configureRngTrigger(self.device, axisNo, lower, upper)
       
    
    def configureRngTriggerEps(self, axisNo, epsilon):
        '''
        Configure hysteresis for range Trigger.

        Parameters
            axisNo	Axis number (0 ... 2)
            epsilon	hysteresis in nm / mdeg
        Returns
            None
        '''
        ANC.configureRngTriggerEps(self.device, axisNo, epsilon)
        
        
    def configureRngTriggerPol(self, axisNo, polarity):
        '''
        Configure lower position for range Trigger.

        Parameters
            axisNo	Axis number (0 ... 2)
            polarity	Polarity of trigger signal when position is between lower and upper Low(0) and High(1)
        Returns
            None
        '''
        ANC.configureRngTriggerPol(self.device, axisNo, polarity)
       
    
    def connect(self, devNo=0):
        '''
        Initializes and connects the selected device. This has to be done before any access to control variables or measured data.

        Parameters
            devNo	Sequence number of the device. Must be smaller than the devCount from the last ANC_discover call. Default: 0
        Returns
            device	Handle to the opened device, NULL on error
        '''
        device = ctypes.c_void_p()
        ANC.connect(devNo, ctypes.byref(device))
        return device
        
        
    def disconnect(self):
        '''
        Closes the connection to the device. The device handle becomes invalid.

        Parameters
            None
        Returns
            None
        '''
        ANC.disconnect(self.device)
       
    
    def discover(self, ifaces=3):
        '''
        The function searches for connected ANC350RES devices on USB and LAN and initializes internal data structures per device. Devices that are in use by another application or PC are not found. The function must be called before connecting to a device and must not be called as long as any devices are connected.

        The number of devices found is returned. In subsequent functions, devices are identified by a sequence number that must be less than the number returned.

        Parameters
            ifaces	Interfaces where devices are to be searched. {None: 0, USB: 1, ethernet: 2, all:3} Default: 3
        Returns
            devCount	number of devices found
        '''
        devCount = ctypes.c_int()
        ANC.discover(ifaces, ctypes.byref(devCount))
        return devCount.value
    
    
    def getActuatorName(self, axisNo):
        '''
        Get the name of the currently selected actuator

        Parameters
            axisNo	Axis number (0 ... 2)
        Returns
            name	Name of the actuator
        '''
        name = ctypes.create_string_buffer(20)
        ANC.getActuatorName(self.device, axisNo, ctypes.byref(name))
        return name.value.decode('utf-8')
        
        
    def getActuatorType(self, axisNo):
        '''
        Get the type of the currently selected actuator

        Parameters
            axisNo	Axis number (0 ... 2)
        Returns
            type_	Type of the actuator {0: linear, 1: goniometer, 2: rotator}
        '''
        type_ = ctypes.c_int()
        ANC.getActuatorType(self.device, axisNo, ctypes.byref(type_))
        return type_.value
       
        
    def getAmplitude(self, axisNo):
        '''
        Reads back the amplitude parameter of an axis.
        
        Parameters
            axisNo	Axis number (0 ... 2)
        Returns
            amplitude	Amplitude V
        '''
        amplitude = ctypes.c_double()
        ANC.getAmplitude(self.device, axisNo, ctypes.byref(amplitude))
        return amplitude.value
    
    
    def getAxisStatus(self, axisNo):
        '''
        Reads status information about an axis of the device.

        Parameters
            axisNo	Axis number (0 ... 2)
        Returns
            connected	Output: If the axis is connected to a sensor.
            enabled	Output: If the axis voltage output is enabled.
            moving	Output: If the axis is moving.
            target	Output: If the target is reached in automatic positioning
            eotFwd	Output: If end of travel detected in forward direction.
            eotBwd	Output: If end of travel detected in backward direction.
            error	Output: If the axis' sensor is in error state.
        '''
        connected = ctypes.c_int()
        enabled = ctypes.c_int()
        moving = ctypes.c_int()
        target = ctypes.c_int()
        eotFwd = ctypes.c_int()
        eotBwd = ctypes.c_int()
        error = ctypes.c_int()

        ANC.getAxisStatus(self.device, axisNo, ctypes.byref(connected), ctypes.byref(enabled), ctypes.byref(moving), ctypes.byref(target), ctypes.byref(eotFwd), ctypes.byref(eotBwd), ctypes.byref(error))
        return connected.value, enabled.value, moving.value, target.value, eotFwd.value, eotBwd.value, error.value
    
    
    def getDeviceConfig(self):
        '''
        Reads static device configuration data

        Parameters
            None
        Returns
            featureSync	"Sync": Ethernet enabled (1) or disabled (0)
            featureLockin	"Lockin": Low power loss measurement enabled (1) or disabled (0)
            featureDuty	"Duty": Duty cycle enabled (1) or disabled (0)
            featureApp	"App": Control by IOS app enabled (1) or disabled (0)
        '''
        features = ctypes.c_int()
        ANC.getDeviceConfig(self.device, features)
        
        featureSync = 0x01&features.value
        featureLockin = (0x02&features.value)/2
        featureDuty = (0x04&features.value)/4
        featureApp = (0x08&features.value)/8
        
        return featureSync, featureLockin, featureDuty, featureApp

    
    def getDeviceInfo(self, devNo=0):
        '''
        Returns available information about a device. The function can not be called before ANC_discover but the devices don't have to be connected . All Pointers to output parameters may be zero to ignore the respective value.

        Parameters
            devNo	Sequence number of the device. Must be smaller than the devCount from the last ANC_discover call. Default: 0
        Returns
            devType	Output: Type of the ANC350 device. {0: Anc350Res, 1:Anc350Num, 2:Anc350Fps, 3:Anc350None}
            id	Output: programmed hardware ID of the device
            serialNo	Output: The device's serial number. The string buffer should be NULL or at least 16 bytes long.
            address	Output: The device's interface address if applicable. Returns the IP address in dotted-decimal notation or the string "USB", respectively. The string buffer should be NULL or at least 16 bytes long.
            connected	Output: If the device is already connected
        '''
        devType = ctypes.c_int()
        id_ = ctypes.c_int()
        serialNo = ctypes.create_string_buffer(16) 
        address = ctypes.create_string_buffer(16) 
        connected = ctypes.c_int()

        ANC.getDeviceInfo(devNo, ctypes.byref(devType), ctypes.byref(id_), ctypes.byref(serialNo), ctypes.byref(address), ctypes.byref(connected))
        return devType.value, id_.value, serialNo.value.decode('utf-8'), address.value.decode('utf-8'), connected.value
    
    
    def getFirmwareVersion(self):
        '''
        Retrieves the version of currently loaded firmware.

        Parameters
            None
        Returns
            version	Output: Version number
        '''
        version = ctypes.c_int()
        ANC.getFirmwareVersion(self.device, ctypes.byref(version))
        return version.value
    
    
    def getFrequency(self, axisNo):
        '''
        Reads back the frequency parameter of an axis.

        Parameters
            axisNo	Axis number (0 ... 2)
        Returns
            frequency	Output: Frequency in Hz
        '''
        frequency = ctypes.c_double()
        ANC.getFrequency(self.device, axisNo, ctypes.byref(frequency))
        return frequency.value
    
    
    def getPosition(self, axisNo):
        '''
        Retrieves the current actuator position. For linear type actuators the position unit is m; for goniometers and rotators it is degree.

        Parameters
            axisNo	Axis number (0 ... 2)
        Returns
            position	Output: Current position [m] or [°]
        '''
        position = ctypes.c_double()
        ANC.getPosition(self.device, axisNo, ctypes.byref(position))
        return position.value
    
    
    def measureCapacitance(self, axisNo):
        '''
        Performs a measurement of the capacitance of the piezo motor and returns the result. If no motor is connected, the result will be 0. The function doesn't return before the measurement is complete; this will take a few seconds of time.

        Parameters
            axisNo	Axis number (0 ... 2)
        Returns
            cap	Output: Capacitance [F]
        '''
        cap = ctypes.c_double()
        ANC.measureCapacitance(self.device, axisNo, ctypes.byref(cap))
        return cap.value
   

    def saveParams(self):
        '''
        Saves parameters to persistent flash memory in the device. They will be present as defaults after the next power-on. The following parameters are affected: Amplitude, frequency, actuator selections as well as Trigger and quadrature settings.

        Parameters
            None
        Returns
            None
        '''
        ANC.saveParams(self.device)
    
    
    def selectActuator(self, axisNo, actuator):
        '''
        Selects the actuator to be used for the axis from actuator presets.

        Parameters
            axisNo	Axis number (0 ... 2)
            actuator	Actuator selection (0 ... 255)
                0: ANPg101res
                1: ANGt101res
                2: ANPx51res
                3: ANPx101res
                4: ANPx121res
                5: ANPx122res
                6: ANPz51res
                7: ANPz101res
                8: ANR50res
                9: ANR51res
                10: ANR101res
                11: Test
        Returns
            None
        '''
        ANC.selectActuator(self.device, axisNo, actuator)
    
    
    def setAmplitude(self, axisNo, amplitude):
        '''
        Sets the amplitude parameter for an axis

        Parameters
            axisNo	Axis number (0 ... 2)
            amplitude	Amplitude in V, internal resolution is 1 mV
        Returns
            None
        '''
        ANC.setAmplitude(self.device, axisNo, ctypes.c_double(amplitude))
   

    def setAxisOutput(self, axisNo, enable, autoDisable):
        '''
        Enables or disables the voltage output of an axis.

        Parameters
            axisNo	Axis number (0 ... 2)
            enable	Enables (1) or disables (0) the voltage output.
            autoDisable	If the voltage output is to be deactivated automatically when end of travel is detected.
        Returns
            None
        '''
        ANC.setAxisOutput(self.device, axisNo, enable, autoDisable)
   

    def setDcVoltage(self, axisNo, voltage):
        '''
        Sets the DC level on the voltage output when no sawtooth based motion is active.

            Parameters
            axisNo	Axis number (0 ... 2)
            voltage	DC output voltage [V], internal resolution is 1 mV
        Returns
            None        
        '''
        ANC.setDcVoltage(self.device, axisNo, ctypes.c_double(voltage))
 

    def setFrequency(self, axisNo, frequency):
        '''
        Sets the frequency parameter for an axis

        Parameters
            axisNo	Axis number (0 ... 2)
            frequency	Frequency in Hz, internal resolution is 1 Hz
        Returns
            None
        '''
        ANC.setFrequency(self.device, axisNo, ctypes.c_double(frequency))
        
   
    def setTargetPosition(self, axisNo, target):
        '''
        Sets the target position for automatic motion, see ANC_startAutoMove. For linear type actuators the position unit is m, for goniometers and rotators it is degree.

        Parameters
            axisNo	Axis number (0 ... 2)
            target	Target position [m] or [°]. Internal resulution is 1 nm or 1 µ°.
        Returns
            None
        '''
        ANC.setTargetPosition(self.device, axisNo, ctypes.c_double(target))
        
        
    def setTargetRange(self, axisNo, targetRg):
        '''
        Defines the range around the target position where the target is considered to be reached.

        Parameters
            axisNo	Axis number (0 ... 2)
            targetRg	Target range [m] or [°]. Internal resulution is 1 nm or 1 µ°.
        Returns
            None
        '''
        ANC.setTargetRange(self.device, axisNo, ctypes.c_double(targetRg))
        
        
    def startAutoMove(self, axisNo, enable, relative):
        '''
        Switches automatic moving (i.e. following the target position) on or off

        Parameters
            axisNo	Axis number (0 ... 2)
            enable	Enables (1) or disables (0) automatic motion
            relative	If the target position is to be interpreted absolute (0) or relative to the current position (1)
        Returns
            None
        '''
        ANC.startAutoMove(self.device, axisNo, enable, relative)
        
   
    def startContinuousMove(self, axisNo, start, backward):
        '''
        Starts or stops continous motion in forward direction. Other kinds of motions are stopped.

        Parameters
            axisNo	Axis number (0 ... 2)
            start	Starts (1) or stops (0) the motion
            backward	If the move direction is forward (0) or backward (1)
        Returns
            None
        '''
        ANC.startContinousMove(self.device, axisNo, start, backward)
        
    def startSingleStep(self, axisNo, backward):
        '''
        Triggers a single step in desired direction.

        Parameters
            axisNo	Axis number (0 ... 2)
            backward	If the step direction is forward (0) or backward (1)
        Returns
            None
        '''
        ANC.startSingleStep(self.device, axisNo, backward)
