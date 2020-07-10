from vengine import engine
from vcomponent import *

r0 = Module('verilog/registor32.v','r0')
r1 = Module('verilog/registor32.v','r1')
r2 = Module('verilog/registor32.v','r2')
r3 = Module('verilog/registor32.v','r3')
r4 = Module('verilog/registor32.v','r4')
r5 = Module('verilog/registor32.v','r5')
r6 = Module('verilog/registor32.v','r6')
r7 = Module('verilog/registor32.v','r7')

dmux = Module('verilog/demux32.v', 'dmux')

m1 = Module('verilog/mux32_32_1.v','m1')
m2 = Module('verilog/mux32_32_1.v','m2')

clk = InputModule('clk',1)
WE = InputModule('WE',1)
RA1 = InputModule('RA1',5)
RA2 = InputModule('RA2',5)
WA = InputModule('WA',5)
WD = InputModule('WD',32)

read1 = Monitor('read1',32)
read2 = Monitor('read2',32)

b1 = Bus(WE.ports,dmux.inputs[0])
b2 = Bus(WA.ports,dmux.inputs[1])

w1 = Wire(dmux.outputs[0][0],r0.inputs[0][0])
w2 = Wire(dmux.outputs[0][1],r1.inputs[0][0])
w3 = Wire(dmux.outputs[0][2],r2.inputs[0][0])
w4 = Wire(dmux.outputs[0][3],r3.inputs[0][0])
w5 = Wire(dmux.outputs[0][4],r4.inputs[0][0])
w6 = Wire(dmux.outputs[0][5],r5.inputs[0][0])
w7 = Wire(dmux.outputs[0][6],r6.inputs[0][0])
w8 = Wire(dmux.outputs[0][7],r7.inputs[0][0])

w11 = Wire(clk.ports[0],r0.inputs[1][0])
w12 = Wire(clk.ports[0],r1.inputs[1][0])
w13 = Wire(clk.ports[0],r2.inputs[1][0])
w14 = Wire(clk.ports[0],r3.inputs[1][0])
w15 = Wire(clk.ports[0],r4.inputs[1][0])
w16 = Wire(clk.ports[0],r5.inputs[1][0])
w17 = Wire(clk.ports[0],r6.inputs[1][0])
w18 = Wire(clk.ports[0],r7.inputs[1][0])

b11 = Bus(WD.ports,r0.inputs[2])
b12 = Bus(WD.ports,r1.inputs[2])
b13 = Bus(WD.ports,r2.inputs[2])
b14 = Bus(WD.ports,r3.inputs[2])
b15 = Bus(WD.ports,r4.inputs[2])
b16 = Bus(WD.ports,r5.inputs[2])
b17 = Bus(WD.ports,r6.inputs[2])
b18 = Bus(WD.ports,r7.inputs[2])

b21 = Bus(r0.outputs[0],m1.inputs[0][32*0:32*1])
b22 = Bus(r1.outputs[0],m1.inputs[0][32*1:32*2])
b23 = Bus(r2.outputs[0],m1.inputs[0][32*2:32*3])
b24 = Bus(r3.outputs[0],m1.inputs[0][32*3:32*4])
b25 = Bus(r4.outputs[0],m1.inputs[0][32*4:32*5])
b26 = Bus(r5.outputs[0],m1.inputs[0][32*5:32*6])
b27 = Bus(r6.outputs[0],m1.inputs[0][32*6:32*7])
b28 = Bus(r7.outputs[0],m1.inputs[0][32*7:32*8])

b31 = Bus(r0.outputs[0],m2.inputs[0][32*0:32*1])
b32 = Bus(r1.outputs[0],m2.inputs[0][32*1:32*2])
b33 = Bus(r2.outputs[0],m2.inputs[0][32*2:32*3])
b34 = Bus(r3.outputs[0],m2.inputs[0][32*3:32*4])
b35 = Bus(r4.outputs[0],m2.inputs[0][32*4:32*5])
b36 = Bus(r5.outputs[0],m2.inputs[0][32*5:32*6])
b37 = Bus(r6.outputs[0],m2.inputs[0][32*6:32*7])
b38 = Bus(r7.outputs[0],m2.inputs[0][32*7:32*8])

b41 = Bus(RA1.ports,m1.inputs[1])
b42 = Bus(RA2.ports,m2.inputs[1])

b51 = Bus(m1.outputs[0],read1.ports)
b52 = Bus(m2.outputs[0],read2.ports)

modules = [r0,r1,r2,r3,r4,r5,r6,r7,dmux,m1,m2]
io_devices = [clk,WE,RA1,RA2,WA,WD,read1,read2]
buses = [b1,b2,b11,b12,b13,b14,b15,b16,b17,b18,b21,b22,b23,b24,b25,b26,b27,b28, \
        b31,b32,b33,b34,b35,b36,b37,b38,b41,b42,b51,b52]
wires = [w1,w2,w3,w4,w5,w6,w7,w8,w11,w12,w13,w14,w15,w16,w17,w18]

layout = Layout(modules, wires, buses, io_devices)

e = engine(layout,None)
e.create_module('regfile.v')

regfile = Module('regfile.v','reg')
e2 = engine(None, regfile)
e2.create_tb('regfile_tb.v')
