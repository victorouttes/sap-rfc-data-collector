# sap-rfc-data-collector

Collect data from SAP tables directly.

## Install
```
pip install sap-rfc-data-collector
```

## Quick start
```
from sap_rfc_data_collector.sap import SAP

runner = SAP(host='host',
             service='service',
             group='group',
             sysname='sysname',
             client='client',
             lang='lang',
             user='user',
             password='password')

# get dataframe from functional location table (IFLO)
df = runner.get_dataframe(
    table='IFLO',
    columns=['TPLNR', 'ZFAMF'],
    where="IWERK = 'CMPN'"
)

print(df.shape)
```
Result:
```
[...]
Aproximate rows collected...68000
Aproximate rows collected...69000
Aproximate rows collected...70000
Aproximate rows collected...71000
(70616, 2)
```

Consult some site (like https://www.sapdatasheet.org) to identify tables and
columns names!

## Requirements
SAP NWRFC SDK 7.50 PL3 or later must be downloaded (SAP partner or customer account required) 
and locally installed.

This project depends on Cython. Some considerations:
* Linux: The GNU C Compiler (gcc) is usually present, or easily available through the package system. 
  On Ubuntu or Debian, for instance, the command sudo apt-get install build-essential will fetch 
  everything you need.
* Mac OS X: To retrieve gcc, one option is to install Apple’s XCode, which can be retrieved from the 
  Mac OS X’s install DVDs or from https://developer.apple.com/.
* Windows: A popular option is to use the open source MinGW (a Windows distribution of gcc). 
  See the appendix for instructions for setting up MinGW manually. Enthought Canopy and Python(x,y) 
  bundle MinGW, but some of the configuration steps in the appendix might still be necessary. 
  Another option is to use Microsoft’s Visual C. One must then use the same version which the installed 
  Python was compiled with.