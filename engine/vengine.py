
import os
import subprocess
from engine.vtemplate import module, testbanch
from engine.vcomponent import *
from engine.vports import *
from engine.utils import *

class engine:
    def __init__(self, layout, module):
        self.layout = layout
        self.module = module

    def create_module(self, name):
        files = [c.file_path for c in self.layout.modules]
        files = list(dict.fromkeys(files))
        port_dict = self.layout.get_all_ports()
        port_dict = combine_ports(port_dict)
        # print(port_dict)
        # port_info = get_port_info(port_dict)
        # print(port_info)
        size_dict = self.layout.get_port_size()
        io_dict = self.layout.get_io_dict()
        # print(io_dict)
        port_list = self.layout.get_port_list()

        module(name, files, self.layout.modules, port_dict, size_dict, io_dict, port_list)

    def create_tb(self, name):
        testbanch(name, self.module.file_path, self.module)

    def run_component(self, component):
        compile_command = 'iverilog ' + component.file_path + ' -o ' + component.file_path.split('.')[0] + '.out'
        run_command = './' + component.file_path.split('.')[0] + '.out'
        execute = subprocess.getoutput(compile_command)
        run_output = subprocess.getoutput(run_command)

        return run_output


    