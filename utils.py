
def combine_ports(port_dict):
    combinations_dict = {}
    for key, val in zip(port_dict,port_dict.values()):
        combinations = []
        for p in val:
            final_equal = []
            equal = []
            temp = None
            for l in p:
                if temp is None:
                    temp = l
                    equal.append(l)
                elif l!=temp:
                    final_equal.append(equal)
                    equal = []
                    temp = l
                    equal.append(l)
                else:
                    equal.append(l)
            final_equal.append(equal)
            combinations.append(final_equal)
        combinations_dict[key] = combinations
    return combinations_dict

def make_port_label(port_list):
    label_list = []
    port_size = []
    for i in port_list:
        labels = []
        size = []
        for j in i:
            labels.append(j[0].label)
            size.append(len(j))
        label_list.append(labels)
        port_size.append(size)
    return label_list, port_size

# def get_size_dict(port_dict):
#     size_dict = {}
#     for ports in port_dict.values():
#         for p in ports:
#             for m in p:


def get_labels_form_dict(port_dict, size_dict):
    label_list = []
    for ports in port_dict.values():
        module_labels = []
        for p in ports:
            labels = []
            for m in p:
                try:
                    name = m[0].module+'_'+m[0].label 
                    if len(m)==size_dict[name]:
                        labels.append(name)
                    elif len(m)<size_dict[name]:
                        if len(m)==1:
                            labels.append(name+'['+str(m[0].id)+']')
                        else:
                            labels.append(name+'['+str(m[-1].id)+':'+str(m[0].id)+']')
                except AttributeError:
                    for n in m:
                        name = n[0].module+'_'+n[0].label
                        if len(n)==size_dict[name]:
                            labels.append(name)
                        elif len(n)<size_dict[name]:
                            if len(n)==1:
                                labels.append(name+'['+str(n[0].id)+']')
                            else:
                                labels.append(name+'['+str(n[-1].id)+':'+str(n[0].id)+']')
                    
            module_labels.append(labels)
        label_list.append(module_labels)
    return label_list

def process_label_list(label_list):
    final_list = []
    for labels in label_list:
        temp = []
        for l in labels:
            if len(l)>1:
                label = '{'
            else:
                label = ''
            for i in l:
                label+=i+','
            if len(l)>1:
                label = label[:-1] + '}'
            else:
                label = label[:-1] 
            temp.append(label)
        final_list.append(temp)
    return final_list

def get_wire_list(port_dict, io_dict):
    wire_list = []
    size = []
    for val in port_dict.values():
        for ports in val:
            for p in ports:
                try:
                    if p[0].type=='output':
                        wire = p[0].module+'_'+p[0].label
                        # wire = p[0].label
                        if not wire in io_dict['output'] and not wire in io_dict['input']:
                            if wire in wire_list:
                                index = wire_list.index(wire)
                                if len(p)>size[index]:
                                    size[index] = len(p)
                            else:
                                wire_list.append(wire)
                                size.append(len(p))
                except:
                    for q in p:
                        if q[0].type=='output':
                            wire = q[0].module+'_'+q[0].label
                            # wire = p[0].label
                            if not wire in io_dict['output'] and not wire in io_dict['input']:
                                if wire in wire_list:
                                    index = wire_list.index(wire)
                                    if len(q)>size[index]:
                                        size[index] = len(q)
                                else:
                                    wire_list.append(wire)
                                    size.append(len(q))    
    return wire_list, size

def get_port_info(port_dict):
    port_info = {}
    for key,val in zip(port_dict,port_dict.values()):
        length = []
        for ports in val:
            for p in ports:
                length.append(len(p))
        port_info[key] = length
    return port_info
