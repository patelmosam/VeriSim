from engine.vports import Port

def verilog_parser(file_path, label):
    inputs = []
    outputs = []
    with open(file_path) as file:
            data = file.read()
            data = data.split('\n')
            for line in data:
                for l in line.split():
                    if l=='module':
                        line = line.replace('(',' ')
                        name = line.split()[1]
                    elif l=='input':
                        size = 0
                        for i in line.split():
                            if i[0]=='[':
                                s = i[1:].replace(':',' ')
                                s = s.split(' ')
                                size = int(s[0]) - int(s[1][:-1])
                            if i!='input' and i[0]!='[':
                                i = i.replace(',','')
                                _input = []
                                for p in range(size+1):
                                    _input.append(Port(i.replace(';',''), 'input', label, p))
                                inputs.append(_input)

                    elif l=='output':
                        size = 0
                        for i in line.split():
                            if i[0]=='[':
                                s = i[1:].replace(':',' ')
                                s = s.split(' ')
                                size = int(s[0]) - int(s[1][:-1])
                            if i!='output' and i!='reg' and i[0]!='[':
                                i = i.replace(',','')
                                _output = []
                                for p in range(size+1):
                                    _output.append(Port(i.replace(';',''), 'output', label, p))
                                outputs.append(_output)
                    
                    elif l=="endmodule":
                        return inputs, outputs, name
    return inputs, outputs, name

# def outfile_parser(file_path):
    # with open(command.split()[-1]) as file:
        #     data = file.read()
        #     data = data.split('\n')
        #     for line in data:
        #         if not line=='':
        #             if line[0]!="#" and line[0]!=":":
        #                 for l in line.split():
        #                     if l=="module,":
        #                         self.name = line.split()[3][1:-1]
        #                     elif l=="/INPUT":
        #                         self.inputs.append(Port(line.split()[-1][1:-1], 'input', self.name, int(line.split()[-2])))
        #                     elif l=="/OUTPUT":
        #                         self.outputs.append(Port(line.split()[-1][1:-1], 'output', self.name, int(line.split()[-2])))