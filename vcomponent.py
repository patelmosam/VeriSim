import subprocess
from vparser import verilog_parser
from vports import *
class Module:
    def __init__(self, file_path, label):
        self.file_path = file_path
        self.label = label
        self.name = ''
        self.inputs = []
        self.outputs = []
        self.inouts = []
        self.make_module()

    def make_module(self):
        command = 'iverilog ' + self.file_path + ' -o ' + self.file_path.split('.')[0] + '.out'
        process = subprocess.getoutput(command)
        self.inputs, self.outputs, self.name = verilog_parser(self.file_path)
        delete = subprocess.getoutput('rm '+ command.split()[-1])

    def run(self):
        compile_command = 'iverilog ' + self.file_path + ' -o ' + self.file_path.split('.')[0] + '.out'
        run_command = './' + self.file_path.split('.')[0] + '.out'
        execute = subprocess.getoutput(compile_command)
        run_output = subprocess.getoutput(run_command)
        return run_output


class Layout:
    def __init__(self, modules, wires, IO_devices):
        self.modules = modules
        self.wires = wires
        self.IO_devices = IO_devices

    # def

class Wire:
    def __init__(self, From, To):
        self.From = From
        self.To = To

    def __str__(self):
        return 'Wire(From: '+ self.From.module+ '->' + self.From.label \
                + ', To: '+ self.To.module +'->'+ self.To.label +')'




if __name__ == '__main__':
    AND = Module('and.v','a')
    in1 = InputComponent('in1',1)
    
    wire = Wire(in1.ports[0], AND.inputs[0])
    # in1.ports[0][1] = '11'
    # for i in AND.outputs:
    #     for j in i:
    #         print(j)