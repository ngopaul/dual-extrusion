G21 ; set units to millimeters
M107
;M104 S200 T1 ; set temperature
G28 ; home all axes

G1 Z5 F5000 ; lift nozzle

;M109 S200 T1 ; wait for temperature to be reached
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
T0
G1 Z0.350 F7800.000
;G1 F1800.000 E-10.00000
;G92 E0
;T1
;G92 E0

;T1
;G1 F1800.000 E-10.00000
G92 E0
T0
G92 E0

M106 S255
G1 Z15.000 F7800.000

G1 X90.000 Y115.000 F2000.000

M106 S255
G1 Z-15.000 F7800.000

G1 X90.000 Y115.000 E10.0000 F100.000
G1 X70.000 Y115.000 E20.0000 F100.000
G1 X70.000 Y95.000 E20.0000 F100.000
G1 X90.000 Y95.000 E20.0000 F100.000
G1 X90.000 Y115.000 E20.0000 F100.000
; move off
G1 X90.000 Y116.000 F2000.000
G1 X91.000 Y116.000 F2000.000

M106 S255
G1 Z2.000 F7800.000

G92 E0
T1
G92 E0

G1 X90.000 Y138.000 F2000.000
G1 X90.000 Y138.000 E10.0000 F100.000
G1 X70.000 Y138.000 E20.0000 F100.000
G1 X70.000 Y118.000 E20.0000 F100.000
G1 X90.000 Y118.000 E20.0000 F100.000
G1 X90.000 Y138.000 E20.0000 F100.000
; move off
G1 X90.000 Y139.000 F2000.000
G1 X91.000 Y139.000 F2000.000

M106 S255
G1 Z15.000 F7800.000

G28
M84