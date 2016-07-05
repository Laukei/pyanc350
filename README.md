# attocube ANC350 Python library

A Python implementation of the C++ header for the attocube ANC350 controller (ANC350lib) plus a more Pythonesque reimagining (PyANC350). Suppports driver versions 2, 3, and 4.

Original version by Rob Heath (rob@robheath.me.uk), updated driver support by Brian Schaefer (bts72@cornell.edu).

## Using the module

### If using v2 of the ANC350 driver:
1. Use `ANC350lib.py` and `PyANC350.py`.
2. Put `anc350v2.dll`, `nhconnect.dll`, and `libusb0.dll` in the same folder as `ANC350lib.py`.

### If using v3 or v4 of the ANC350 driver:
1. Use `ANC350v4lib.py` and `PyANC350v4.py`
2. Put `anc350v3.dll` or `anc350v4.dll` and `libusb0.dll` in the same folder as `ANC350v4lib.py`.

