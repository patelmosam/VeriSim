import subprocess
from vparser import verilog_parser
from vports import *
from utils import combine_ports

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
    
    def get_port_list(self):
        port_list = []
        for m in self.modules:
            oports = [pout for pout in m.outputs]
            iports = [pin for pin in m.inputs]
            port_list.append(oports+iports)
        return port_list

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
                    if b.From[i].isequal(p):
                        connected_ports.append(b.From[i])
                    elif b.To[i].isequal(p):
                        if b.From[i].module=='InputModule':
                            connected_ports.append(b.To[i])
                        else:
                            connected_ports.append(b.From[i])
            for w in self.wires:
                if w.From.isequal(p):
                    connected_ports.append(w.From)
                elif w.To.isequal(p):
                    if w.From.module=='InputModule':
                        connected_ports.append(w.To)
                    else:
                        connected_ports.append(w.From)
        return connected_ports

    def get_connected_ports(self, module):
        in_connections = []
        out_connections = []
        for in_port in module.inputs:
            in_connections.append(self.connected_module_bus(in_port))
        for out_port in module.outputs:
            out_connections.append(self.connected_module_bus(out_port))
        
        return out_connections + in_connections 

    def get_all_ports(self):
        module_dict = {}
        for m in self.modules:
            module_dict[m.label] = self.get_connected_ports(m)
        return module_dict

    def get_port_size(self):
        size_dict = {}
        for m in self.modules:
            for i in m.inputs:
                size_dict[i[0].module+'_'+i[0].label] = len(i)
            for o in m.outputs:
                size_dict[o[0].module+'_'+o[0].label] = len(i)
        return size_dict

    def get_io_dict(self):
        io_dict = {'input':[], 'isize':[], 'output':[], 'osize':[]}
        wire_list = []
        in_module = []
        out_module = []
        for w in self.wires:
            if w.From.module == 'InputModule':
                io_dict['input'].append(w.To.module+'_'+w.To.label)
                io_dict['isize'].append(1)
                in_module.append(w.To.module)
            if w.To.module == 'monitor':
                io_dict['output'].append(w.From.module+'_'+w.From.label)
                io_dict['osize'].append(1)
                out_module.append(w.From.module)
            else:
                wire_list.append(w)
        
        bus_list = []
        bus_size = []
        for b in self.buses:
            if b.From[0].module == 'InputModule':
                io_dict['input'].append(b.To[0].module+'_'+b.To[0].label)
                io_dict['isize'].append(b.get_size())
                in_module.append(b.To[0].module)
            if b.To[0].module == 'monitor':
                io_dict['output'].append(b.From[0].module+'_'+b.From[0].label)
                io_dict['osize'].append(b.get_size())
                out_module.append(b.From[0].module)
            else:
                bus_list.append(b)
                bus_size.append(b.get_size())
        return io_dict

class Wire:
    def __init__(self, From, To):
        self.From = From
        self.To = To
        self.check_ports()

    def check_ports(self):
        if not isinstance(self.From, Port) or not isinstance(self.To, Port):
            raise TypeError('must be port')
        if self.From == self.To:
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
    AND1 = Module('verilog/and.v','a2')
    NOT = Module('verilog/not.v','n1')
    in1 = InputModule('in1',2)
    in2 = InputModule('in2',2)
    m1 = Monitor('m1',2)
    m2 = Monitor('m2',1)
    b1 = Bus(in1.ports, AND.inputs[0])
    b2 = Bus(in2.ports, AND.inputs[1])
    b4 = Bus(in1.ports, AND1.inputs[0])
    b5 = Bus(in2.ports, AND1.inputs[1])
    b3 = Bus(AND.outputs[0], m1.ports)
    w1 = Wire(AND1.outputs[0][0],NOT.inputs[0][0])
    w2 = Wire(NOT.outputs[0][0],m2.ports[0])

    L = Layout([AND, AND1,NOT],[w1,w2],[b1,b2,b3,b4,b5],[in1,in2,m1])
    # ports = L.connected_module_bus(AND.inputs[0])
    fdict = L.get_all_ports()
    flist = combine_ports(fdict)
    print(flist)
    # for l in fdict['a1']:
    #     for j in l:
    #         print(j)