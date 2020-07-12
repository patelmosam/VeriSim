import sys
sys.path.insert(1, '/home/mosam/ICR/VeriSim/engine')

from vengine import engine
from vcomponent import *

path = 'example/verilog/gates/'
path1 = 'example/verilog/gates/examples/'

And1 = Module(path + 'and.v','a1')
And2 = Module(path + 'and.v','a2')
Or1 = Module(path + 'or.v','o1')
Or2 = Module(path + 'or.v','o2')
in1 = InputModule('i1',2)
in2 = InputModule('i2',2)
m1 = Monitor('m1',1)
m2 = Monitor('m2',1)
b1 = Bus(in1.ports, And1.inputs[0])
b2 = Bus(in1.ports, And2.inputs[0])
b3 = Bus(in2.ports, And1.inputs[1])
b4 = Bus(in2.ports, And2.inputs[1])
# print(type(And1.outputs[0][0]), type(Or1.inputs[0][0]))
w1 = Wire(And1.outputs[0][0], Or1.inputs[0][0])
w2 = Wire(And2.outputs[0][0], Or1.inputs[1][0])
w3 = Wire(And1.outputs[0][1], Or2.inputs[0][0])
w4 = Wire(And2.outputs[0][1], Or2.inputs[1][0])
w5 = Wire(Or1.outputs[0][0], m1.ports[0])
w6 = Wire(Or2.outputs[0][0], m2.ports[0])
L1 = Layout([Or1,Or2,And1,And2],[w1,w2,w3,w4,w5,w6],[b1,b2,b3,b4],[in1,in2,m1,m2])
e = engine(L1,None)
#out = e.run_component(mux)
e.create_module(path1 + 'andor.v')
# e.create_tb('')
and_or = Module(path1 + 'andor.v', 'andor')
# print(and_or)
e2 = engine(None, and_or)
e2.create_tb(path1 + 'andor_tb.v')
# print(out)