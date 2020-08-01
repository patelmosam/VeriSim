# from PySide2.QtWidgets import QWidget, QOpenGLWidget
from PySide2.QtCore import QRect, QSize, Qt, QPoint, QMargins, QLine, QRectF
from PySide2.QtGui import QColor, QPen, QPainter, QMouseEvent, QPolygon, QPainterPath, QVector2D, QPainterPathStroker, QFont
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
        self.pins = []

    def pins(self):
        raise NotImplementedError

    def paint(self, painter):
        raise NotImplementedError

    def draw_pins(self, painter):
        for pin in self.pins:
            point = pin.position
            if pin.type == 'input':
                painter.drawLine(point.x(), point.y(), point.x()+10, point.y())
            elif pin.type == 'output':
                painter.drawLine(point.x()-10, point.y(), point.x(), point.y())


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
        self.H = (max([self.input_pins, self.output_pins]) + 1)*(self.min_dist)
        self.SCALE = 1
        self.SIZE = QSize(self.SCALE*100, self.SCALE*self.H)
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.pins = self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        pins = []
        for i,s in zip(range(self.input_pins),self.module.inputs):
            pins.append(Pin(None, QVector2D(-1, 0), QPoint(-10, (i+1)*(bb.height() / (self.input_pins + 1))), 'input', len(s)))
        for i,s in zip(range(self.output_pins),self.module.outputs):
            pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width()+10, (i+1)*(bb.height() / (self.output_pins + 1))), 'output', len(s)))
        return pins

    def paint(self, painter):
        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(Qt.white)
        font = QFont()
        font.setPointSize(self.SCALE + 10)

        path = QPainterPath()
        s = self.SIZE
        path.moveTo(QPoint())
        path.lineTo(QPoint(s.width(), 0))
        path.lineTo(QPoint(s.width(), s.height()))
        path.lineTo(QPoint(0, s.height()))
        path.closeSubpath()
        painter.drawPath(path)
        painter.setFont(font)
        painter.drawText(QPoint(0,s.height()+20), self.module.name)
        self.draw_pins(painter)

    def resize(self, plus_or_minus):
        if not plus_or_minus:
            self.SCALE += 0.5
        else:
            self.SCALE -= 0.5
        self.SIZE = QSize(self.SCALE*100, self.SCALE*self.H)
        self.bounding_box = QRect(self.bounding_box.topLeft(), self.SIZE)
        self.pins = self.get_pins()

class NotElement(Element):
    SCALE = 1
    SIZE = QSize(50, 0.75*50)

    def __init__(self, label):
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.file = "components/gates/not.v"
        self.label = label
        self.module = Module(self.file, self.label)
        self.pins = self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        pins = []
        pins.append(Pin(None, QVector2D(-1, 0), QPoint(-10, bb.height() / 2), 'input'))
        pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width()+10, bb.height() / 2), 'output'))
        return pins

    def paint(self, painter):
        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(Qt.white)
        font = QFont()
        font.setPointSize(self.SCALE + 10)

        path = QPainterPath()
        s = self.SIZE
        path.moveTo(QPoint())
        path.lineTo(QPoint(s.width() - 5, s.height() / 2))
        path.lineTo(QPoint(0, s.height()))
        path.closeSubpath()
        painter.drawPath(path)
        painter.setFont(font)
        painter.drawText(QPoint(0,s.height()+20), self.module.name)
        painter.drawEllipse(QPoint(s.width() - 2, s.height() / 2), 3, 3)
        self.draw_pins(painter)

    def resize(self, plus_or_minus):
        if not plus_or_minus:
            self.SCALE += 0.5
        else:
            self.SCALE -= 0.5
        self.SIZE = QSize(self.SCALE*50, self.SCALE*0.75*50)
        self.bounding_box = QRect(self.bounding_box.topLeft(), self.SIZE)
        self.pins = self.get_pins()

class AndElement(Element):
    SCALE = 1
    SIZE = QSize(50, 0.75*50)

    def __init__(self, label):
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.file = "components/gates/and.v"
        self.label = label
        self.module = Module(self.file, self.label)
        self.pins = self.get_pins()
        

    def get_pins(self):
        bb = self.bounding_box
        pins = []
        pins.append(Pin(None, QVector2D(-1, 0), QPoint(-10, bb.height() / 3), 'input'))
        pins.append(Pin(None, QVector2D(-1, 0), QPoint(-10, 2 * bb.height() / 3), 'input'))
        pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width()+10, bb.height() / 2), 'output'))
        return pins

    def paint(self, painter):
        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(Qt.white)
        font = QFont()
        font.setPointSize(self.SCALE + 10)

        path = QPainterPath()
        s = self.SIZE
        path.moveTo(QPoint())
        path.lineTo(QPoint(s.width() / 2, 0))
        path.arcTo(QRectF(QPoint(), self.SIZE), 90.0, -180.0)
        path.lineTo(QPoint(s.width() / 2, s.height()))
        path.lineTo(QPoint(0, s.height()))
        path.closeSubpath()
        painter.drawPath(path)
        self.draw_pins(painter)
        painter.setFont(font)
        painter.drawText(QPoint(0,s.height()+20), self.module.name)

    def resize(self, plus_or_minus):
        if not plus_or_minus:
            self.SCALE += 0.5
        else:
            self.SCALE -= 0.5
        self.SIZE = QSize(self.SCALE*50, self.SCALE*0.75*50)
        self.bounding_box = QRect(self.bounding_box.topLeft(), self.SIZE)
        self.pins = self.get_pins()
      

class OrElement(Element):
    SCALE = 1
    SIZE = QSize(50, 0.75*50)

    def __init__(self, label):
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.file = "components/gates/or.v"
        self.label = label
        self.module = Module(self.file, self.label)
        self.pins = self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        pins = []
        pins.append(Pin(None, QVector2D(-1, 0), QPoint(-10+bb.width()/8, bb.height() / 3), 'input'))
        pins.append(Pin(None, QVector2D(-1, 0), QPoint(-10+bb.width()/8, 2 * bb.height() / 3), 'input'))
        pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width()+10, bb.height() / 2), 'output'))
        return pins

    def paint(self, painter):
        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(Qt.white)
        font = QFont()
        font.setPointSize(self.SCALE + 10)

        path = QPainterPath()
        s = self.SIZE

        r1 = QSize(2*s.width()+(s.width()/7), 2*s.height())

        path.moveTo(QPoint())
        path.arcTo(QRectF(QPoint(-s.width(),0), r1), 90.0, -60.0)
        path.arcTo(QRectF(QPoint(-s.width(),-s.height()), r1), -30.0, -60.0)
        path.arcTo(QRectF(QPoint(-s.width()*2,-s.height()/2), r1), -30.0, 60.0)
        
        path.closeSubpath()
        painter.drawPath(path)
        self.draw_pins(painter)
        painter.setFont(font)
        painter.drawText(QPoint(0,s.height()+20), self.module.name)

    def resize(self, plus_or_minus):
        if not plus_or_minus:
            self.SCALE += 0.5
        else:
            self.SCALE -= 0.5
        self.SIZE = QSize(self.SCALE*50, self.SCALE*0.75*50)
        self.bounding_box = QRect(self.bounding_box.topLeft(), self.SIZE)
        self.pins = self.get_pins()

class InputElement(Element):
    SCALE = 1
    SIZE = QSize(50, 50)

    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.module = InputModule(self.label, self.size)
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.pins = self.get_pins()

    def get_pins(self):
        bb = self.bounding_box
        pins = []
        pins.append(Pin(None, QVector2D(1, 0), QPoint(bb.width()+10, bb.height() / 2), 'output', self.size))
        return pins

    def paint(self, painter):
        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(Qt.white)
        font = QFont()
        font.setPointSize(self.SCALE + 10)

        s = self.SIZE
        painter.drawEllipse(QRect(QPoint(), self.SIZE))
        self.draw_pins(painter)
        painter.setFont(font)
        painter.drawText(QPoint(0,s.height()+20), self.module.name)

    def resize(self, plus_or_minus):
        if not plus_or_minus:
            self.SCALE += 0.5
        else:
            self.SCALE -= 0.5
        self.SIZE = QSize(self.SCALE*50, self.SCALE*50)
        self.bounding_box = QRect(self.bounding_box.topLeft(), self.SIZE)
        self.pins = self.get_pins()

class MonitorElement(Element):
    SCALE = 1
    SIZE = QSize(50, 50)

    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.module = Monitor(self.label, self.size)
        self.min_dist = 25
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0
        self.pins = self.get_pins()        

    def get_pins(self):
        bb = self.bounding_box
        pins = []
        pins.append(Pin(None, QVector2D(-1, 0), QPoint(-10, bb.height() / 2), 'input', self.size))
        return pins

    def paint(self, painter):
        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(Qt.white)
        font = QFont()
        font.setPointSize(self.SCALE + 10)

        s = self.SIZE
        painter.drawEllipse(QRect(QPoint(), self.SIZE))
        self.draw_pins(painter)
        painter.setFont(font)
        painter.drawText(QPoint(0,s.height()+20), self.module.name)

    def resize(self, plus_or_minus):
        if not plus_or_minus:
            self.SCALE += 0.5
        else:
            self.SCALE -= 0.5
        self.SIZE = QSize(self.SCALE*50, self.SCALE*50)
        self.bounding_box = QRect(self.bounding_box.topLeft(), self.SIZE)
        self.pins = self.get_pins()

class WireElement:
    def __init__(self, connection, points):
        self.label = None
        self.connection = connection
        self.points = points

class BusElement:
    def __init__(self, connection, points, size):
        self.label = None
        self.connection = connection
        self.points = points
        self.size = size
