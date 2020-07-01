import os

def module(name, files, modules, wires, IO_devices):
    with open(name, 'w') as tb:
        # include statements
        for i in files:
            tb.write('`include \"'+ i + '\" \n')
        tb.write('\n')

        #data extraction
        port_list = []
        for c in modules:
            oports = [pout for pout in c.outputs]
            iports = [pin for pin in c.inputs]
            port_list.append(oports+iports)
            
        # module defination
        io_dict = {'input':[],'output':[]}
        for w in wires:
            if w.From.module == 'InputComponent':
                io_dict['input'].append(w.To.label)
            elif w.To.module == 'monitor':
                io_dict['output'].append(w.From.label)

        tb.write('module ' + name.split('.')[0] + '(')
        for o in io_dict['output']:
            tb.write(o+', ')
        for i in io_dict['input']:
            tb.write(i+', ')
        tb.seek(tb.tell()-2,os.SEEK_SET)
        tb.write(');\n')

        # input/output declaration
        module_input = []
        for c in modules:
            c.inputs.sort()
            input_port = [s for s in c.inputs if s.label in io_dict['input']]
            module_input.append(input_port)
            size_list = [s.size for s in input_port] 
            size_list = list(dict.fromkeys(size_list))
            # print(size_list)
            for s in size_list:
                tb.write('input ')
                if s!=1:
                    tb.write('['+str(s-1)+':0] ')
                for i in input_port:
                    if i.size==s:
                        tb.write(i.label+', ')            
                tb.seek(tb.tell()-2,os.SEEK_SET)
                tb.write(';\n')

        # wire declaration
        module_output = []
        for c in modules:
            c.outputs.sort()
            output_port = [s for s in c.outputs if s.label in io_dict['output']]
            module_output.append(output_port)
            size_list = [s.size for s in output_port] 
            # print(size_list)
            for s in size_list:
                tb.write('output ')
                if s!=1:
                    tb.write('['+str(s-1)+':0] ')
                for i in output_port:
                    if i.size==s:
                        tb.write(i.label+', ')            
                tb.seek(tb.tell()-2,os.SEEK_SET)
                tb.write(';\n')
        tb.write('\n')
       
        # wire declaration
        module_wire = []
        for c in modules:
            c.outputs.sort()
            wire_port = []
            for wo, wi in zip(c.outputs, c.inputs):
                if not wo.label in io_dict['output']:
                    wire_port.append(wo)
                    module_wire.append(wo)
                if not wi.label in io_dict['input']:
                    module_wire.append(wi)
            size_list = [s.size for s in wire_port] 
            # print(size_list)
            for s in size_list:
                tb.write('wire ')
                if s!=1:
                    tb.write('['+str(s-1)+':0] ')
                for i in wire_port:
                    if i.size==s:
                        tb.write(c.name+'_'+i.label+', ')            
                tb.seek(tb.tell()-2,os.SEEK_SET)
                tb.write(';\n')
        tb.write('\n')
        
        port_info = []
        for ports, iports, oports in zip(port_list, module_input, module_output):
            port_dict = {}
            for port in ports:
                # print(port.label)
                if port.type == 'output':
                    if port in module_wire:
                        port_dict[port.label] = port.module + '_' + port.label
                    elif port in oports:
                        port_dict[port.label] = port.label
                elif port.type == 'input':
                    if port in module_wire:
                        for w in wires:
                            if w.To.isequal(port):
                                port_dict[port.label] = w.From.module +'_'+ w.From.label
                    elif port in iports:
                        port_dict[port.label] = port.label
            port_info.append([port_dict])

        # module instantiation
        for c, i in zip(modules, range(len(modules))): 
            tb.write(c.name +' '+ c.name+'_'+'uut(')
            for pkey, pval in zip(port_info[i][0], port_info[i][0].values()):
                tb.write('.'+ pkey + '('+ pval +'), ')
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(');\n')
        tb.write('\n')

        tb.write('endmodule')

def testbanch(name, files, modules):
    with open(name, 'w') as tb:
        # include statements
        for i in files:
            tb.write('`include \"'+ i + '\" \n')
        tb.write('\n')

        # module defination
        tb.write('module ' + name.split('.')[0] + ';\n')
            
        # reg declaration
        for c in modules:
            c.inputs.sort()
            size_list = [s.size for s in c.inputs] 
            size_list = list(dict.fromkeys(size_list))
            # print(size_list)
            for s in size_list:
                tb.write('reg ')
                if s!=1:
                    tb.write('['+str(s-1)+':0] ')
                for i in c.inputs:
                    if i.size==s:
                        tb.write(i.label+', ')            
                tb.seek(tb.tell()-2,os.SEEK_SET)
                tb.write(';\n')

        # wire declaration
        for c in modules:
            c.outputs.sort()
            size_list = [s.size for s in c.outputs] 
            size_list = list(dict.fromkeys(size_list))
            # print(size_list)
            for s in size_list:
                tb.write('wire ')
                if s!=1:
                    tb.write('['+str(s-1)+':0] ')
                for i in c.outputs:
                    if i.size==s:
                        tb.write(i.label+', ')            
                tb.seek(tb.tell()-2,os.SEEK_SET)
                tb.write(';\n')
        tb.write('\n')

        # module instantiation
        for c in modules: 
            tb.write(c.name + ' uut(')
            for out in c.outputs:
                tb.write('.'+out.label + '('+out.label+'), ')
            for i in c.inputs:
                tb.write('.'+i.label + '('+i.label+'), ')
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(');\n')
        tb.write('\n')

        # stimulas code
        tb.write('initial begin\n\
            \n // add your stimulas code here \n\n')
        tb.write('end\n')

        tb.write('\n')
        tb.write('endmodule')

