# from PySide2.QtWidgets import QWidget, QOpenGLWidget
from PySide2.QtCore import QRect, QSize, Qt, QPoint, QMargins, QLine, QRectF
from PySide2.QtGui import QColor, QPen, QPainter, QMouseEvent, QPolygon, QPainterPath, QVector2D, QPainterPathStroker


class Element:
    def __init__(self):
        # self.descriptor = descriptor
        self.bounding_box = QRect()
        self.schematic = None
        self.oriantation = 0

    def pins(self):
        raise NotImplementedError

    def paint(self, painter):
        raise NotImplementedError


class Pin:
    def __init__(self, pin, direction, position, _type):
        self.pin = pin
        self.direction = direction
        self.position = position
        self.type = _type

class GeneralElement(Element):
    # SIZE = QSize(100, 75)

    def __init__(self, input_pins, output_pins):
        # super().__init__(descriptor)
        self.min_dist = 25
        H = (max([input_pins, output_pins]) + 1)*(self.min_dist)
        self.SIZE = QSize(100, H)
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.input_pins = input_pins
        self.output_pins = output_pins
        self.oriantation = 0

    def pins(self):
        bb = self.bounding_box
        for i in range(self.input_pins):
            yield Pin(None, QVector2D(-1, 0), QPoint(0, (i+1)*(bb.height() / (self.input_pins + 1))), 'input')
        for i in range(self.output_pins):
            yield Pin(None, QVector2D(1, 0), QPoint(bb.width(), (i+1)*(bb.height() / (self.output_pins + 1))), 'output')

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

    def __init__(self):
        # super().__init__(descriptor)
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0

    def pins(self):
        bb = self.bounding_box
        yield Pin(None, QVector2D(-1, 0), QPoint(0, bb.height() / 2), 'input')
        yield Pin(None, QVector2D(1, 0), QPoint(bb.width(), bb.height() / 2), 'output')

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

    def __init__(self):
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0

    def pins(self):
        bb = self.bounding_box
        yield Pin(None, QVector2D(-1, 0), QPoint(0, bb.height() / 3), 'input')
        yield Pin(None, QVector2D(-1, 0), QPoint(0, 2 * bb.height() / 3), 'input')
        yield Pin(None, QVector2D(1, 0), QPoint(bb.width(), bb.height() / 2), 'output')

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

        painter.drawEllipse(QPoint(s.width(), s.height() / 2), 3, 3)

class OrElement(Element):
    SIZE = QSize(100, 75)

    def __init__(self):
        self.bounding_box = QRect(QPoint(), self.SIZE)
        self.oriantation = 0

    def pins(self):
        bb = self.bounding_box
        yield Pin(None, QVector2D(-1, 0), QPoint(bb.width()/8, bb.height() / 3), 'input')
        yield Pin(None, QVector2D(-1, 0), QPoint(bb.width()/8, 2 * bb.height() / 3), 'input')
        yield Pin(None, QVector2D(1, 0), QPoint(bb.width(), bb.height() / 2), 'output')

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


