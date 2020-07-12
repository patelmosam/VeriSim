import sys
sys.path.insert(1, '/home/mosam/ICR/VeriSim/engine')

from vengine import engine
from vcomponent import *

path = 'example/verilog/ALU/'

add_sub = Module(path + 'add_sub.v','adder')
logic = Module(path + 'logic.v','logic')
shifter = Module(path + 'shifter32.v','shifter')
mux = Module(path + 'mux32_4_2.v','mux')
X = InputModule('x',32)
Y = InputModule('y',32)
C = InputModule('control',5)
cin = InputModule('cin', 1)
over = Monitor('overflow',1)
out = Monitor('out',32)

b01 = Bus(Y.ports[16:], add_sub.inputs[0][:16])
b02 = Bus(X.ports[:16], add_sub.inputs[0][16:])
b03 = Bus(X.ports[16:], add_sub.inputs[1][:16])
b04 = Bus(Y.ports[:16], add_sub.inputs[1][16:])
w1 = Wire(cin.ports[0], add_sub.inputs[2][0])
w2 = Wire(C.ports[4], add_sub.inputs[3][0])

b3 = Bus(X.ports, logic.inputs[0])
b4 = Bus(Y.ports, logic.inputs[1])
b5 = Bus(C.ports[2:4], logic.inputs[2])

b6 = Bus(X.ports, shifter.inputs[0])
b7 = Bus(Y.ports, shifter.inputs[1])
b8 = Bus(C.ports[2:4], shifter.inputs[2])

b9 = Bus(shifter.outputs[0], mux.inputs[0])
b10 = Bus(add_sub.outputs[0], mux.inputs[1])
b11 = Bus(add_sub.outputs[0], mux.inputs[2])
b12 = Bus(logic.outputs[0], mux.inputs[3])
b13 = Bus(C.ports[0:2], mux.inputs[4])

b14 = Bus(mux.outputs[0], out.ports)
w3 = Wire(add_sub.outputs[1][0], over.ports[0])

modules = [add_sub, logic, shifter, mux]
wires = [w1,w2,w3] 
buses = [b01,b02,b03,b04,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14]
io_devices = [X, Y, C, cin, over, out]

layout = Layout(modules, wires, buses, io_devices)

e = engine(layout, None)
e.create_module(path + 'alu32_test.v')

alu = Module(path + 'alu32_test.v', 'alu')
e1 = engine(None, alu)
e1.create_tb(path + 'alutb_test.v')

