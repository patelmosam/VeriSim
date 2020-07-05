

class Port:
    def __init__(self, label, Type, module, id):
        self.label = label
        self.type = Type
        self.module = module
        self.id = id
        # self.size = size

    def __eq__(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Port)):
            return False
        if  self.label == other.label and \
            self.module == other.module and \
            self.type == other.type:
            return True
        return False

    def isequal(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Port)):
            return False
        if  self.label == other.label and \
            self.module == other.module and \
            self.type == other.type and \
            self.id == other.id:
            return True
        return False

    def __str__(self):
        return "Port([label: "+ self.label + ', ' \
                'type: '+ self.type + ', ' \
                'module: '+ self.module +', '+ \
                'id: '+ str(self.id) + '])'

class InputModule:
    def __init__(self, label, size):
        self.label = label
        # self.no_of_ports = no_of_ports
        self.ports = []
        self.value = []
        self.size = size
        self.make_ports()

    def make_ports(self):
        for i in range(self.size):
            self.ports.append(Port(self.label,'output','InputModule', i))
            self.value.append(None)

class Monitor:
    def __init__(self, label, size):
        # self.no_of_ports = no_of_ports
        self.label = label
        self.size = size
        self.ports = []
        self.make_ports()

    def make_ports(self):
        for i in range(self.size):
            self.ports.append(Port(self.label,'input','monitor', i))
