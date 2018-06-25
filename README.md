RD transform
=======

This package can be used to transform coordinates in the Rijksdriehoeksstelsel(RD) to those in the WGS86 system.
It is based on the methods discussed in [this paper](https://media.thomasv.nl/2015/07/Transformatieformules.pdf) by ing. F.H. Schreutelkamp and ir. G.L. Strang van Hees.

Install
--------
Clone the repository and use the setup.py file to install the package.

```
python setup.py install
```

Usage
------
This package contains a total of four functions, which can be used to transform RD-coordinates to WGS86 coordinates and vice-versa. Simply import the package and provide the functions with either a tuple, a numpy array or pandas DataFrame with coordinates.

```python
from RD_transform import RD_to_UTM, RD_to_latlon, UTM_to_RD, latlon_to_RD

RD_coords = [150000,400000]
latlon_coords = RD_to_latlon(RD_coords)
```