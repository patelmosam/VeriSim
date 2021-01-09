import subprocess
from src.engine.parser import verilog_parser
from src.engine.ports import *
from src.engine.utils import combine_ports

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

    # def connected_module_bus(self, bus_port):
    #     connected_ports = []
    #     c_ports_list = []
    #     bus_ptr = 0
    #     wire_ptr = 0
    #     for b in self.buses:
    #         c_ports = []
    #         if len(bus_port)==b.get_size():
    #             for p,i in zip(bus_port,range(b.get_size())):
    #                 if b.From[i].isequal(p):
    #                     if b.To[i].module == 'monitor':
    #                         c_ports.append(b.To[i])
    #                     else:
    #                         c_ports.append(b.From[i])
    #                 elif b.To[i].isequal(p):
    #                     c_ports.append(b.From[i])
    #             if len(c_ports)>0:
    #                 connected_ports.append(c_ports)
    #         elif len(bus_port) > b.get_size():
    #             if bus_port[bus_ptr] == b.From[0]:
    #                 for p1,i1 in zip(bus_port[bus_ptr:],range(b.get_size())):
    #                     if b.To[i1].module == 'monitor':
    #                         c_ports.append(b.To[i1])
    #                     else:
    #                         c_ports.append(b.From[i1])
    #                     bus_ptr = p1.id + 1
    #                 c_ports_list.append(c_ports)
    #             elif bus_port[bus_ptr] == b.To[0]:
    #                 for p1,i1 in zip(bus_port[bus_ptr:],range(b.get_size())):
    #                     c_ports.append(b.From[i1])
    #                     bus_ptr = p1.id + 1
    #                 c_ports_list.append(c_ports)
    #             if bus_ptr==len(bus_port):
    #                 bus_ptr = 0

    #     for w in self.wires:
    #         c_ports = []
    #         # for p in bus_port:
    #         if w.From.isequal(p[wire_ptr]):
    #             if w.To.module == 'monitor':
    #                 c_ports.append(w.To)
    #                 wire_ptr+=1
    #             else:
    #                 c_ports.append(w.From)
    #                 wire_ptr+=1
    #         elif w.To.isequal(p[wire_ptr]):
    #             c_ports.append(w.From)
    #             wire_ptr+=1
    #         if len(c_ports)>0:
    #             connected_ports.append(c_ports)
        
    #     if len(connected_ports)==0:
    #         connected_ports.append(c_ports_list)
    #     return connected_ports[0]

    def connected_module(self, bus_port, call):
        port_id = [i for i in range(len(bus_port))]
        c_ports = [None for _ in range(len(bus_port))]

        for w in self.wires:
            for p in port_id:
                if bus_port[p].isequal(w.From):
                    if w.To.module == 'monitor':
                        c_ports[p] = w.To
                        port_id.remove(p)
                        break
                    else:
                        c_ports[p] = w.From
                        port_id.remove(p)
                        break
                elif bus_port[p].isequal(w.To):
                    c_ports[p] = w.From
                    port_id.remove(p)
                    break

        if None in c_ports:
            for bus in self.buses:
                for i in range(bus.get_size()):
                    for p in port_id:
                        if bus_port[p].isequal(bus.From[i]):
                            if bus.To[i].module == 'monitor':
                                c_ports[p] = bus.To[i]
                                port_id.remove(p)
                            else:
                                c_ports[p] = bus.From[i]
                                port_id.remove(p)
                        elif bus_port[p].isequal(bus.To[i]):
                            c_ports[p] = bus.From[i]
                            port_id.remove(p)

        if call == 'output':
            for p in port_id:
                port = Port('open','output', bus_port[0].module, 0)
                c_ports[p] = port
        
        return c_ports

    def get_connected_ports(self, module):
        in_connections = []
        out_connections = []
        for in_port in module.inputs:
            in_connections.append(self.connected_module(in_port, 'input'))
        for out_port in module.outputs:
            out_connections.append(self.connected_module(out_port, 'output'))
        
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
                size_dict[o[0].module+'_'+o[0].label] = len(o)
        for m in self.IO_devices:
            size_dict[m.ports[0].module+'_'+m.ports[0].label] = len(m.ports)
        return size_dict

    def get_io_dict(self):
        io_dict = {'input':[], 'isize':[], 'output':[], 'osize':[]}
        for io in self.IO_devices:
            if io.name=='Input':
                io_dict['input'].append('Input_'+io.ports[0].label)
                io_dict['isize'].append(len(io.ports))
            if io.name=='Monitor':
                io_dict['output'].append('monitor_'+io.ports[0].label)
                io_dict['osize'].append(len(io.ports))
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
    