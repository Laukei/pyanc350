#
# PyANC350 example file
#   by Rob Heath
#

from pyanc350.v2 import Positioner
import time

ax = {'x':0,'y':1,'z':2}
#define a dict of axes to make things simpler

anc = Positioner()
#instantiate positioner as anc
print('-------------------------------------------------------------')
print('capacitances:')
for axis in sorted(ax.keys()):
    print(axis,anc.capMeasure(ax[axis]))
print('-------------------------------------------------------------')
print('setting static amplitude to 2V')
anc.staticAmplitude(2000)
#set staticAmplitude to 2V to ensure accurate positioning info
print('-------------------------------------------------------------')
print('moving to x = 2mm')
anc.moveAbsolute(ax['x'],2000000)

#check what's happening
time.sleep(0.5)
state = 1
while state == 1:
    newstate = anc.getStatus(ax['x']) #find bitmask of status
    if newstate == 1:
        print('axis moving, currently at',anc.getPosition(ax['x']))
    elif newstate == 0:
        print('axis arrived at',anc.getPosition(ax['x']))
    else:
        print('axis has value',newstate)
    state = newstate
    time.sleep(0.5)

print('and moving y:')
anc.moveAbsolute(ax['y'],2000000)
time.sleep(0.5)
state = 1
while state == 1:
    newstate = anc.getStatus(ax['y']) #find bitmask of status
    if newstate == 1:
        print('axis moving, currently at',anc.getPosition(ax['y']))
    elif newstate == 0:
        print('axis arrived at',anc.getPosition(ax['y']))
    else:
        print('axis has value',newstate)
    state = newstate
    time.sleep(0.5)
    
print('-------obtaining all possible get\'able values for x---------')
#get every possible get'able value
print('getAcInEnable',anc.getAcInEnable(ax['x']))
print('getAmplitude',anc.getAmplitude(ax['x']))
print('getBandwidthLimitEnable',anc.getBandwidthLimitEnable(ax['x']))
print('getDcInEnable',anc.getDcInEnable(ax['x']))
print('getDcLevel',anc.getDcLevel(ax['x']))
print('getFrequency',anc.getFrequency(ax['x']))
print('getIntEnable',anc.getIntEnable(ax['x']))
print('getPosition',anc.getPosition(ax['x']))
print('getReference',anc.getReference(ax['x']))
print('getReferenceRotCount',anc.getReferenceRotCount(ax['x']))
print('getRotCount',anc.getRotCount(ax['x']))
print('getSpeed',anc.getSpeed(ax['x']))
print('getStatus',anc.getStatus(ax['x']))
print('getStepwidth',anc.getStepwidth(ax['x']))
print('-------------------------------------------------------------')

print('starting test of setTargetPos and moveAbsoluteSync')
anc.setTargetPos(ax['x'],2500000)
anc.setTargetPos(ax['y'],2500000)
anc.moveAbsoluteSync(3)

statex, statey = 1, 1
while statex == 1 or statey == 1:
    print('x:',anc.getPosition(ax['x']),'y:',anc.getPosition(ax['y']))
    time.sleep(0.5)
    statex = anc.getStatus(ax['x'])
    statey = anc.getStatus(ax['y'])
    print('statex:',statex,'statey:',statey)
print('arrived by moveAbsoluteSync')
print('could use a function to create the bitmask for moveAbsoluteSync!')
print('-------------------------------------------------------------')
print('testing \'functions for manual positioning\'')
anc.frequency(ax['x'],50)
print('set frequency to 50Hz')
for i in range(30):
    anc.moveSingleStep(ax['x'],1)
    time.sleep(0.1)
print('arrived at:',anc.getPosition(ax['x']),'after 30 pulses')
anc.moveContinuous(ax['x'],1)
print('waiting 3 seconds...')
time.sleep(5)
anc.stopMoving(ax['x'])
print('and stopped at',anc.getPosition(ax['x']))
print('set frequency to 200Hz')
anc.frequency(ax['x'],200)
anc.moveContinuous(ax['x'],1)
print('waiting 3 seconds...')
time.sleep(5)
anc.stopMoving(ax['x'])
print('testing amplitude control')
anc.amplitudeControl(ax['x'],1)
print('amp control set to Amplitude (open loop)')
anc.dcLevel(ax['x'],10000)
print('amplitude set to:',anc.getDcLevel(ax['x']))
anc.moveContinuous(ax['x'],0)
time.sleep(3)
anc.stopMoving(ax['x'])
anc.amplitudeControl(ax['x'],0)
print('amp control set to Speed')
anc.moveContinuous(ax['x'],0)
for i in range(6):
    print('speed',anc.getSpeed(ax['x']))
    time.sleep(0.5)
anc.stopMoving(ax['x'])
anc.amplitudeControl(ax['x'],2)
print('amp control set to Stepwidth')
anc.moveContinuous(ax['x'],1)
for i in range(6):
    print('stepwidth',anc.getStepwidth(ax['x']))
    time.sleep(0.5)
anc.stopMoving(ax['x'])



print('-------------------------------------------------------------')
print('no point testing trigger configuration (chapter 7): no triggers!')
print('-------------------------------------------------------------')
print('closing connection...')
anc.close()
print('-------------------------------------------------------------')
