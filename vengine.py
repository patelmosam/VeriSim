
import os
import subprocess
from vtemplate import module, testbanch
from vcomponent import *
from vports import *

class engine:
    def __init__(self, layout, module):
        self.layout = layout
        self.module = module

    def create_module(self, name):
        files = [c.file_path for c in self.layout.modules]

        module(name, files, self.layout.modules, self.layout.wires, self.layout.buses, self.layout.IO_devices)

    def create_tb(self, name):
        template.testbanch(name, self.module.file_path, self.module)

    def run_component(self, component):
        compile_command = 'iverilog ' + component.file_path + ' -o ' + component.file_path.split('.')[0] + '.out'
        run_command = './' + component.file_path.split('.')[0] + '.out'
        execute = subprocess.getoutput(compile_command)
        run_output = subprocess.getoutput(run_command)

        return run_output

if __name__=='__main__':
    And1 = Module('verilog/and.v','a1')
    And2 = Module('verilog/and.v','a2')
    Or1 = Module('verilog/or.v','o1')
    Or2 = Module('verilog/or.v','o2')
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
    L1 = Layout([And1,And2,Or1,Or2],[w1,w2,w3,w4,w5,w6],[b1,b2,b3,b4],[in1,in2,m1,m2])
    e = engine(L1,None)
    #out = e.run_component(mux)
    e.create_module('verilog/andor.v')

    # and_not = Component('andnot.v')
    # e2 = engine(None, and_not)
    # e2.create_tb('andnot_tb.v')
    # print(out)