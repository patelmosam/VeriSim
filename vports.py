

class Port:
    def __init__(self, label, Type, module):
        self.label = label
        self.type = Type
        self.module = module
        # self.size = size
    
    def __lt__(self, other):
        return self.size < other.size

    def __gt__(self, other):
        return self.size > other.size

    def __eq__(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Port)):
            return False
        if self.size == other.size and \
            self.label == other.label and \
            self.module == other.module and \
            self.type == other.type:
            return True
        return False

    def isequal(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Port)):
            return False
        if self.size == other.size and \
            self.label == other.label and \
            self.module == other.module and \
            self.type == other.type:
            return True
        return False

    def __str__(self):
        return "[port: "+ self.label + ', ' \
                'type: '+ self.type + ', ' \
                'component: '+ self.module +  ']'

class InputComponent:
    def __init__(self, label, size):
        self.label = label
        # self.no_of_ports = no_of_ports
        self.ports = []
        self.size = size
        self.make_ports()

    def make_ports(self):
        for i in range(self.size):
            self.ports.append([Port(self.label,'input','InputComponent'),None])

class Monitor:
    def __init__(self, label, size):
        # self.no_of_ports = no_of_ports
        self.label = label
        self.size = size
        self.ports = []
        self.make_ports()

    def make_ports(self):
        for i in range(self.size):
            self.ports.append(Port(self.label,'output','monitor'))
