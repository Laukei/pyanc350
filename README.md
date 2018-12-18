# pyanc350 attocube ANC350 Python library

pyanc350 is a Python wrapper for controlling attocube systems AG's ANC350 piezoelectric control electronics. It contains an implementation of the C++ header for the attocube ANC350 controller (ANC350lib) plus a more Pythonesque reimagining (PyANC350). It suppports DLL versions 2, 3, and 4.

The original implementation by Rob Heath (rob@robheath.me.uk) was updated to support later ANC350 libraries by Brian Schaefer (bts72@cornell.edu). Both of these were updated for Python 3.x and packaged as a proper Python module in December 2018.

## Installation

The package is on PyPI. To install via pip:

`pip install pyanc350`

Alternatively, you can download the repository and use it directly.

## Usage

The wrapper needs the attocube-provided DLLs to talk to the ANC350 hardware.

#### If using v2 of the ANC350 library:

Put `anc350v2.dll`, `nhconnect.dll`, and `libusb0.dll` in the same folder as your program.

#### If using v3 or v4 of the ANC350 library:

Put `anc350v3.dll` or `anc350v4.dll` and `libusb0.dll` in the same folder as your program.

### Import syntax:

If using v2: `from pyanc350.v2 import Positioner`

If using v3: `from pyanc350.v3 import Positioner`

If using v4: `from pyanc350.v4 import Positioner`

If using multiple, the cleanest way is to import the top-level module and use that:

```python
import pyanc350

p2 = pyanc350.v2.Positioner()
p3 = pyanc350.v3.Positioner()
p4 = pyanc350.v4.Positioner()
```