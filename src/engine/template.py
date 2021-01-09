import os
from src.engine.utils import *

def module(name, files, modules, port_dict, size_dict, io_dict, port_list):
    
    label_list, port_size = make_port_label(port_list)
    # print(label_list, port_size)
    out_labels = get_labels_form_dict(port_dict, size_dict)
    # print(out_labels)
    out_final = process_label_list(out_labels)
    # print(out_final)
    wires_label, wires_size = get_wire_list(port_dict, io_dict) 
    # print(wires_label,wires_size)

    isize = list(dict.fromkeys(io_dict['isize']))
    osize = list(dict.fromkeys(io_dict['osize']))
    wsize = list(dict.fromkeys(wires_size))
    '''-------------------------------------------------------------------------------------'''

    with open(name, 'w') as tb:

        ''' include statements'''
        for i in files:
            tb.write('`include \"'+ i + '\" \n')
        tb.write('\n')
                
        # module defination
        name = name.split('/')[-1]
        tb.write('module ' + name.split('.')[0]) 
        if(len(io_dict['output'])>0 and len(io_dict['input'])>0):
            tb.write("(")
            for o in io_dict['output']:
                tb.write(o+', ')
            for i in io_dict['input']:
                tb.write(i+', ')
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(');\n')
        else:
            tb.write(';')
        tb.write('\n')

        for si in isize:
            tb.write('input ')
            if si!=1:
                tb.write('['+str(si-1)+':0] ')
            for i, s in zip(io_dict['input'], io_dict['isize']):
                if s==si:
                    tb.write(i+', ')            
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(';\n')

        for so in osize:
            tb.write('output ')
            if so!=1:
                tb.write('['+str(so-1)+':0] ')
            for o, s in zip(io_dict['output'], io_dict['osize']):
                if s==so:
                    tb.write(o+', ')            
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(';\n')
        tb.write('\n')

        for sw in wsize:
            tb.write('wire ')
            if sw!=1:
                tb.write('['+str(sw-1)+':0] ')
            for label, size in zip(wires_label, wires_size):
                if size==sw:
                    tb.write(label+', ')            
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(';\n')
        tb.write('\n')

        # module instantiation
        for c, l, i in zip(modules, label_list, out_final):
            tb.write(c.name +' '+ c.label +'(')
            for label, olabel in zip(l,i):
                tb.write('.'+ label + '('+olabel+'), ')
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(');\n')
        tb.write('\n')

        tb.write('endmodule')

def testbanch(name, files, module):
    with open(name, 'w') as tb:
        # include statements
        
        tb.write('`include \"'+ files + '\" \n')
        tb.write('\n')

        # module defination
        name = name.split('/')[-1]
        tb.write('module ' + name.split('.')[0] + ';\n')
            
        # reg declaration
        isize, osize = [], []
        for i in module.inputs:
            isize.append(len(i))
        for o in module.outputs:
            osize.append(len(o))
        isize = list(dict.fromkeys(isize))
        osize = list(dict.fromkeys(osize))
      
        for s in isize:
            tb.write('reg ')
            if s!=1:
                tb.write('['+str(s-1)+':0] ')
            for i in module.inputs:
                if len(i)==s:
                    tb.write(i[0].label+', ')            
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(';\n')

        # wire declaration
        for s in osize:
            tb.write('wire ')
            if s!=1:
                tb.write('['+str(s-1)+':0] ')
            for i in module.outputs:
                if len(i)==s:
                    tb.write(i[0].label+', ')            
            tb.seek(tb.tell()-2,os.SEEK_SET)
            tb.write(';\n')
        tb.write('\n')

        # module instantiation
        tb.write(module.name + ' uut(')
        for out in module.outputs:
            tb.write('.'+out[0].label + '('+out[0].label+'), ')
        for i in module.inputs:
            tb.write('.'+i[0].label + '('+i[0].label+'), ')
        tb.seek(tb.tell()-2,os.SEEK_SET)
        tb.write(');\n')
        tb.write('\n')

        # stimulas code
        tb.write('initial begin\n\
            \n // add your stimulas code here \n\n')
        tb.write('end\n')

        tb.write('\n')
        tb.write('endmodule')

