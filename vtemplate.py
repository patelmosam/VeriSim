import os

def module(name, files, modules, wires, buses, IO_devices):
    port_list = []
    for c in modules:
        oports = [pout for pout in c.outputs]
        iports = [pin for pin in c.inputs]
        port_list.append(oports+iports)
    print(port_list)
    io_dict = {'input':[], 'isize':[], 'output':[], 'osize':[]}
    wire_list = []
    in_module = []
    out_module = []
    for w in wires:
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
    for b in buses:
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
    print(in_module, out_module)

    with open(name, 'w') as tb:
        # include statements
        
        for i in files:
            tb.write('`include \"'+ i + '\" \n')
        tb.write('\n')
                
        # module defination
        
        tb.write('module ' + name.split('.')[0] + '(')
        for o in io_dict['output']:
            tb.write(o+', ')
        for i in io_dict['input']:
            tb.write(i+', ')
        tb.seek(tb.tell()-2,os.SEEK_SET)
        tb.write(');\n')

        # input/output declaration
        for i, s in zip(io_dict['input'], io_dict['isize']):
            tb.write('input ')
            if s!=1:
                tb.write('['+str(s-1)+':0] ')
                tb.write(i + ', ')            
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(';\n')

        # output declaration
        for i, s in zip(io_dict['output'], io_dict['osize']):
            tb.write('output ')
            if s!=1:
                tb.write('['+str(s-1)+':0] ')
                tb.write(i + ', ') 
            else:
                tb.write(i + ', ')           
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(';\n')

       
        # # wire declaration
        # module_wire = []
        # for c in modules:
        #     c.outputs.sort()
        #     wire_port = []
        #     for wo, wi in zip(c.outputs, c.inputs):
        #         if not wo.label in io_dict['output']:
        #             wire_port.append(wo)
        #             module_wire.append(wo)
        #         if not wi.label in io_dict['input']:
        #             module_wire.append(wi)
        #     size_list = [s.size for s in wire_port] 
        #     # print(size_list)
        #     for s in size_list:
        #         tb.write('wire ')
        #         if s!=1:
        #             tb.write('['+str(s-1)+':0] ')
        #         for i in wire_port:
        #             if i.size==s:
        #                 tb.write(c.name+'_'+i.label+', ')            
        #         tb.seek(tb.tell()-2,os.SEEK_SET)
        #         tb.write(';\n')
        # tb.write('\n')
        
        # port_info = []
        # for ports, iports, oports in zip(port_list, module_input, module_output):
        #     port_dict = {}
        #     for port in ports:
        #         # print(port.label)
        #         if port.type == 'output':
        #             if port in module_wire:
        #                 port_dict[port.label] = port.module + '_' + port.label
        #             elif port in oports:
        #                 port_dict[port.label] = port.label
        #         elif port.type == 'input':
        #             if port in module_wire:
        #                 for w in wires:
        #                     if w.To.isequal(port):
        #                         port_dict[port.label] = w.From.module +'_'+ w.From.label
        #             elif port in iports:
        #                 port_dict[port.label] = port.label
        #     port_info.append([port_dict])

        # # module instantiation
        # for c, i in zip(modules, range(len(modules))): 
        #     tb.write(c.name +' '+ c.name+'_'+'uut(')
        #     for pkey, pval in zip(port_info[i][0], port_info[i][0].values()):
        #         tb.write('.'+ pkey + '('+ pval +'), ')
        #     tb.seek(tb.tell()-2,os.SEEK_SET)
        #     tb.write(');\n')
        # tb.write('\n')

        # tb.write('endmodule')

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

