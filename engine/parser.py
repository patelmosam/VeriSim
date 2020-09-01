# verilog parser v2.0

from engine.ports import Port

def verilog_parser(file_path, label):
    inputs = []
    outputs = []
    with open(file_path) as file:
        data = file.read()
        data = data.split('\n')
        for line in data:
            line = line.strip()

            if(line[:4]=="wire " or line[:3]=="reg "):
                break

            if(line[:2]!="//"):
                is_module = line.find("module")
                is_input = line.find("input")
                is_output = line.find("output")
                is_comment = line.find("//")
                if(is_comment>0):
                    line = line[:is_comment]
                    line = line.strip()

                if(is_module==0):
                    name = line.replace("("," ").split()[1].strip()

                if(is_input>=0):
                    osb, csb = line.find("["), line.find("]")
                    if(osb>=0 and csb >=0):
                        r = line[osb+1:csb].replace(":"," ").split(" ")
                        size = abs(int(r[0]) - int(r[-1]))
                    else:
                        size = 0
                    port_name = line.split(" ")[-1].strip(";").strip(",")
                    _input = []
                    for p in range(size+1):
                        _input.append(Port(port_name, 'input', label, p))
                    inputs.append(_input)

                if(is_output>=0):
                    osb, csb = line.find("["), line.find("]")
                    if(osb>=0 and csb >=0):
                        r = line[osb+1:csb].replace(":"," ").split(" ")
                        size = abs(int(r[0]) - int(r[-1]))
                    else:
                        size = 0
                    port_name = line.split(" ")[-1].strip(";").strip(",")
                    _output = []
                    for p in range(size+1):
                        _output.append(Port(port_name, 'input', label, p))
                    outputs.append(_output)

    return inputs, outputs, name
