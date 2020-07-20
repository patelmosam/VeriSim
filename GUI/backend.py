from GUI.elements import *
from engine.vcomponent import Module, Wire
from GUI.schematicWindow import SchematicEditor as se

def get_label(name, label_dict):
    pass

def get_elements(elements_list):
    elements = []
    io_elements = []
    for ele in elements_list:
        if isinstance(ele, (InputElement,MonitorElement)):
            io_elements.append(ele.module)
        else:
            elements.append(ele.module)
    return elements, io_elements
    
def get_wires(wire_list):
    wires = []
    for w in wire_list:
        in_module = w.connection.In_module.module
        in_pin = w.connection.In_pin
        out_module = w.connection.Out_module.module
        out_pin = w.connection.Out_pin
        if isinstance(in_module,(InputModule)):
            From = in_module.ports[in_pin]
        else:
            try:
                offset = len(in_module.inputs)
                From = in_module.outputs[in_pin-offset][0]
            except:
                print(in_pin, in_module.name)
                raise IndexError
        if isinstance(out_module,(Monitor)):
            To = out_module.ports[out_pin]
        else:
            try:
                To = out_module.inputs[out_pin][0]
            except:
                print(out_pin, out_module.name)
                raise IndexError
        wires.append(Wire(From, To))
    return wires