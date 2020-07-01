
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
        module(name, files, self.layout.modules, self.layout.wires, self.layout.IO_devices)

    def create_tb(self, name):
        template.testbanch(name, self.module.file_path, self.module)

    def run_component(self, component):
        compile_command = 'iverilog ' + component.file_path + ' -o ' + component.file_path.split('.')[0] + '.out'
        run_command = './' + component.file_path.split('.')[0] + '.out'
        execute = subprocess.getoutput(compile_command)
        run_output = subprocess.getoutput(run_command)

        return run_output

if __name__=='__main__':
    And1 = Module('and.v','a1')
    And2 = Module('and.v','a2')
    Not1 = Module('not.v','n1')
    Not2 = Module('not.v','n2')
    Or = Module('or.v','o1')
    in1 = InputComponent('i1',1)
    in2 = InputComponent('i2',1)
    monitor = Monitor(1,1)
    w1 = Wire(in1.ports[0][0], And1.inputs[0])
    w2 = Wire(in2.ports[0][0], And2.inputs[1])
    w3 = Wire(in1.ports[0][0], Not1.inputs[0])
    w4 = Wire(in2.ports[0][0], Not2.inputs[0])
    w5 = Wire(Not1.outputs[0], And2.inputs[0])
    w6 = Wire(Not2.outputs[0], And2.inputs[1])
    w7 = Wire(And1.outputs[0], Or.inputs[0])
    w8 = Wire(And2.outputs[0], Or.inputs[1])
    w9 = Wire(Or.outputs[0], monitor.ports[0])
    L1 = Layout([And1, And2, Not1, Not2, Or], [w1, w2, w3, w4, w5, w6, w7, w8, w9], [in1, in2, monitor])
    e = engine(L1,None)
    #out = e.run_component(mux)
    e.create_module('andnot.v')

    # and_not = Component('andnot.v')
    # e2 = engine(None, and_not)
    # e2.create_tb('andnot_tb.v')
    # print(out)