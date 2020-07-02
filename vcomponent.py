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
        self.inputs, self.outputs, self.name = verilog_parser(self.file_path, self.label)
        delete = subprocess.getoutput('rm '+ command.split()[-1])

    def run(self):
        compile_command = 'iverilog ' + self.file_path + ' -o ' + self.file_path.split('.')[0] + '.out'
        run_command = './' + self.file_path.split('.')[0] + '.out'
        execute = subprocess.getoutput(compile_command)
        run_output = subprocess.getoutput(run_command)
        return run_output


class Layout:
    def __init__(self, modules, wires, buses, IO_devices):
        self.modules = modules
        self.wires = wires
        self.buses = buses
        self.IO_devices = IO_devices

    def get_module(self, module_label):
        for m in self.modules:
            if m.label==module_label:
                return m
            else:
                return None

    def connected_module_wire(self, port):
        for w in wires:
            if w.From.label==port.label:
                return w.From
            elif w.To.label==port.label:
                return w.To
            else:
                return None

    def connected_module_bus(self, bus_port):
        connected_ports = []
        for p in bus_port:
            for b in self.buses:
                for i in range(b.get_size()):
                    if b.From[i].label == p.label:
                        connected_ports.append(b.From[i])
                        break
                    elif b.To[i].label == p.label:
                        connected_ports.append(b.To[i])
                        break
            for w in self.wires:
                if w.From.label == p.label:
                    connected_ports.append(w.From)
                elif w.To.label == p.label:
                    connected_ports.append(w.To)
        return connected_ports

class Wire:
    def __init__(self, From, To):
        self.From = From
        self.To = To
        self.check_ports()

    def check_ports(self):
        if not isinstance(self.From, Port) or not isinstance(self.To, Port):
            raise TypeError('must be port')
        if self.From.isequal(self.To):
            raise TypeError('can not connect to same port')

    def __str__(self):
        return 'Wire(From: '+ self.From.module+ '->' + self.From.label \
                + ', To: '+ self.To.module +'->'+ self.To.label +')'

class Bus:
    def __init__(self, From, To):
        self.From = From
        self.To = To
        self.check_ports()

    def check_ports(self):
        try:
            if not isinstance(self.From,list) or not isinstance(self.To,list):
                raise TypeError('must be a bus')
            elif len(self.From)!=len(self.To):
                raise TypeError('length of the ports must be same')
            for p, q in zip(self.From, self.To):
                if not isinstance(p,Port) or not isinstance(q,Port):
                    raise TypeError('must be a port')
        except TypeError as t:
            raise t
            
    def get_size(self):
        return len(self.From)
           

if __name__ == '__main__':
    AND = Module('verilog/and.v','a1')
    AND = Module('verilog/and.v','a2')
    in1 = InputModule('in1',2)
    in2 = InputModule('in2',2)
    m1 = Monitor('m1',2)
    b1 = Bus(in1.ports, AND.inputs[0])
    b2 = Bus(in2.ports, AND.inputs[1])
    b3 = Bus(AND.outputs[0], m1.ports)

    L = Layout([AND],[],[b1,b2,b3],[])
    ports = L.connected_module_bus(AND.inputs[0])
    print(ports[0],ports[1])
