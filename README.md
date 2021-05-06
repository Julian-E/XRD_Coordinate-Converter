# XRD_Coordinate-Converter


This script will convert dummy H-atoms from CSh-Measurements from the Cartesian coordinate system to a cell dependent Fractional coordinate system.
Afterwards, it will sign in the dummy H-atoms into the choosen .res-file.
Therefore this script has to be run in the SAME directory as 2 files:

1. File: Example.xyz
The format of you xyz file has to be like :

13
commentline
Metall x y z
Donoratom x y z 
Donoratom x y z
Donoratom x y z 
Donoratom x y z 
Donoratom x y z 
Donoratom x y z 
H x y z
H x y z
H x y z
H x y z
H x y z
H x y z

However, the script will only write the dummy H-Atoms into the choosen .res-file, so if your coordination sphere isn't present in the .xyz-file it WOULD NOT matter. 
Thats just for you, to check if the coordinates were converted correctly. Nevertheless, the first two lines will be taken out of account during conversion!!!
So make sure your first atom starts at line 3.

2. File: Example.res
The name of the .res-file does NOT have to be the same as the .xyz-file.

!!!!!!!!!!!!!!!!!!!!!!!!!ATTENTION!!!!!!!!!!!!!!!!!!!!!!!!!
!!!Note, that the script will modify your choosen .res-file, so you might want to save the original one before!!!!
