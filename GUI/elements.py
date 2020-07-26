# from PySide2.QtWidgets import QWidget, QOpenGLWidget
from PySide2.QtCore import QRect, QSize, Qt, QPoint, QMargins, QLine, QRectF
from PySide2.QtGui import QColor, QPen, QPainter, QMouseEvent, QPolygon, QPainterPath, QVector2D, QPainterPathStroker
from engine.component import Module
from engine.ports import *

class Element:
    def __init__(self, label):
        # self.descriptor = descriptor
        self.bounding_box = QRect()
        self.schematic = None
        self.oriantation = 0
        self.file = None
        self.label = label
        self.module = Module(self.file, self.label)

    def pins(self):
        raise NotImplementedError

    def paint(self, painter):
        raise NotImplementedError

    # def get_label()


class Pin:
    def __init__(self, pin, direction, position, _type, size=1):
        self.pin = pin
        self.direction = direction
        self.position = position
        self.type = _type
        self.size = size

class connection:
    def __init__(self, in_module, in_pin, out_module, out_pin):
        self.In_module = in_module
        self.In_pin = in_pin
        self.Out_module = out_module
        self.Out_pin = out_pin

class GeneralElement(Element):
    # SIZE = QSize(100, 75)

    def __init__(self, file_path, label):
        self.file = file_path
        self.label = label
        self.module = Module(self.file, self.label)
        self.input_pins = len(self.module.inputs)
        self.output_pins = len(self.module.outputs)
        self.min_dist = 25
        H = (max([self.input_pins, self.output_pins]) + 1)*(self.min_dist)
        self.SIZE = QSize(100, H)
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.pins = []
        self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        for i,s in zip(range(self.input_pins),self.module.inputs):
            self.pins.append(Pin(None, QVector2D(-1, 0), QPoint(0, (i+1)*(bb.height() / (self.input_pins + 1))), 'input', len(s)))
        for i,s in zip(range(self.output_pins),self.module.outputs):
            self.pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width(), (i+1)*(bb.height() / (self.output_pins + 1))), 'output', len(s)))
 

    def paint(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.white)

        path = QPainterPath()
        s = self.SIZE
        path.moveTo(QPoint())
        path.lineTo(QPoint(s.width() - 5, 0))
        path.lineTo(QPoint(s.width() - 5, s.height()))
        path.lineTo(QPoint(0, s.height()))
        path.closeSubpath()
        painter.drawPath(path)

        # painter.drawEllipse(QPoint(s.width() - 2, s.height() / 2), 3, 3)

class NotElement(Element):
    SIZE = QSize(100, 75)

    def __init__(self, label):
        # super().__init__(descriptor)
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.file = "components/gates/not.v"
        self.label = label
        self.module = Module(self.file, self.label)
        self.pins = []
        self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        self.pins.append(Pin(None, QVector2D(-1, 0), QPoint(0, bb.height() / 2), 'input'))
        self.pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width(), bb.height() / 2), 'output'))

    def paint(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.white)

        path = QPainterPath()
        s = self.SIZE
        path.moveTo(QPoint())
        path.lineTo(QPoint(s.width() - 5, s.height() / 2))
        path.lineTo(QPoint(0, s.height()))
        path.closeSubpath()
        painter.drawPath(path)

        painter.drawEllipse(QPoint(s.width() - 2, s.height() / 2), 3, 3)

class AndElement(Element):
    SIZE = QSize(100, 75)

    def __init__(self, label):
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.file = "components/gates/and.v"
        self.label = label
        self.module = Module(self.file, self.label)
        self.pins = []
        self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        self.pins.append(Pin(None, QVector2D(-1, 0), QPoint(0, bb.height() / 3), 'input'))
        self.pins.append(Pin(None, QVector2D(-1, 0), QPoint(0, 2 * bb.height() / 3), 'input'))
        self.pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width(), bb.height() / 2), 'output'))

    def paint(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.white)

        path = QPainterPath()
        s = self.SIZE
        path.moveTo(QPoint())
        path.lineTo(QPoint(s.width() / 2, 0))
        path.arcTo(QRectF(QPoint(), self.SIZE), 90.0, -180.0)
        path.lineTo(QPoint(s.width() / 2, s.height()))
        path.lineTo(QPoint(0, s.height()))
        path.closeSubpath()
        painter.drawPath(path)

        # painter.drawEllipse(QPoint(s.width(), s.height() / 2), 3, 3)

class OrElement(Element):
    SIZE = QSize(100, 75)

    def __init__(self, label):
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.file = "components/gates/or.v"
        self.label = label
        self.module = Module(self.file, self.label)
        self.pins = []
        self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        self.pins.append(Pin(None, QVector2D(-1, 0), QPoint(bb.width()/8, bb.height() / 3), 'input'))
        self.pins.append(Pin(None, QVector2D(-1, 0), QPoint(bb.width()/8, 2 * bb.height() / 3), 'input'))
        self.pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width(), bb.height() / 2), 'output'))

    def paint(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.white)

        path = QPainterPath()
        s = self.SIZE

        r1 = QSize(2*s.width()+(s.width()/7), 2*s.height())

        path.moveTo(QPoint())
        # path.lineTo(QPoint(s.width() / 2, 0))
        path.arcTo(QRectF(QPoint(-s.width(),0), r1), 90.0, -60.0)
        path.arcTo(QRectF(QPoint(-s.width(),-s.height()), r1), -30.0, -60.0)
        
        # path.lineTo(QPoint(s.width() / 2, s.height()))
        # path.lineTo(QPoint(0, s.height()))
        path.arcTo(QRectF(QPoint(-s.width()*2,-s.height()/2), r1), -30.0, 60.0)
        
        path.closeSubpath()
        painter.drawPath(path)

        painter.drawEllipse(QPoint(s.width() - 2, s.height() / 2), 3, 3)

class InputElement(Element):
    SIZE = QSize(100, 75)

    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.module = InputModule(self.label, self.size)
        self.min_dist = 25
        # H = (self.size + 1)*(self.min_dist)
        # self.SIZE = QSize(100, H)
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.pins = []
        self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        self.pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width(), bb.height() / 2), 'output', self.size))

    def paint(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.white)

        path = QPainterPath()
        s = self.SIZE
        path.moveTo(QPoint())
        path.lineTo(QPoint(s.width() - 5, 0))
        path.lineTo(QPoint(s.width() - 5, s.height()))
        path.lineTo(QPoint(0, s.height()))
        path.closeSubpath()
        painter.drawPath(path)

class MonitorElement(Element):
    SIZE = QSize(100, 75)

    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.module = Monitor(self.label, self.size)
        self.min_dist = 25
        # H = (self.size + 1)*(self.min_dist)
        # self.SIZE = QSize(100, H)
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.pins = []
        self.get_pins()        

    def get_pins(self):
        bb = self.bounding_box
        self.pins.append(Pin(None, QVector2D(-1, 0), QPoint(0, bb.height() / 2), 'input', self.size))

    def paint(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.white)

        path = QPainterPath()
        s = self.SIZE
        path.moveTo(QPoint())
        path.lineTo(QPoint(s.width() - 5, 0))
        path.lineTo(QPoint(s.width() - 5, s.height()))
        path.lineTo(QPoint(0, s.height()))
        path.closeSubpath()
        painter.drawPath(path)

class WireElement:
    def __init__(self, connection, points):
        self.label = None#get_label('wire')
        self.connection = connection
        self.points = points

class BusElement:
    def __init__(self, connection, points, size):
        self.label = None
        self.connection = connection
        self.points = points
        self.size = size
