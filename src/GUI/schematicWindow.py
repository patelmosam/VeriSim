from PySide2.QtWidgets import QWidget, QOpenGLWidget
from PySide2.QtCore import QRect, QSize, Qt, QPoint, QMargins, QLine
from PySide2.QtGui import QColor, QPen, QPainter, QMouseEvent, QPolygon, QPainterPath, QVector2D, QPainterPathStroker

from src.GUI.elements import *
from src.GUI.schematicUtils import *

def _closest_point(line, point):
    d = QVector2D(line.p2() - line.p1())
    d.normalize()
    v = QVector2D(point - line.p1())
    return line.p1() + (d * QVector2D.dotProduct(d, v)).toPoint()


def _is_point_on_line(line, point):
    return QVector2D(line.p1() - point).length() + QVector2D(line.p2() - point).length() == QVector2D(line.p2() - line.p1()).length()


class SchematicEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

        self.elements = list()
        self.wires = list()
        self.buses = list()
        self.pins = dict()

        self.guidepoints = list() # unused
        self.guidelines = list()
        self._ghost_wire = None
        self.wiring_mode = False

        self._wire_start = False
        self.is_bus = False
        self.wire_tip = None
        self.bus_size = None

        self.select_rect = None

        self.selected_elements = list()
        self.moved = False
        self.grabbed_element = None
        self.grab_offset = None
        
        self.start_element = None
        self.pin_index = None
        self.label_dict = {'module':[], 'io':[], 'wire':[]}
        self.highlight_pin = None
        self.get_pins()

    def get_pins(self):
        for element in self.elements:
            self.pins[element] = []
            for pin in element.pins:
                p = pin.position + element.bounding_box.topLeft()
                self.pins[element].append(p)

    def update_pins(self, element):
        self.pins[element] = []
        for pin in element.pins:
            p = pin.position + element.bounding_box.topLeft()
            self.pins[element].append(p)

    def _draw_wire(self, painter, line, ghost, pensize=2):

        fill_color = QColor(0, 0, 0)
        outline_color = QColor(0, 0, 0)

        if ghost:
            fill_color.setAlphaF(0.5)
            outline_color.setAlphaF(0.5)

        painter.setPen(QPen(outline_color, pensize))
        # painter.fillPath(stroke, fill_color)
        for i in range(len(line)-1):
            painter.drawLine(line[i],line[i+1])

    def _draw_wires(self, painter, wires, pensize=2):

            p = QPen(Qt.red, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)

            # stroker = QPainterPathStroker(p)
            # stroke = stroker.createStroke(path).simplified()

            fill_color = QColor(255, 0, 0)
            outline_color = QColor(255, 0, 0)

            painter.setPen(QPen(outline_color, pensize))
            # painter.fillPath(stroke, fill_color)
            # painter.drawPath(path)
            for wire in wires:
                for i in range(len(wire.points)-1):
                    painter.drawLine(wire.points[i],wire.points[i+1])

    def _highlight_pin(self, painter):
        fill_color = QColor(255, 255, 255)
        outline_color = QColor(255, 0, 0)
        painter.setBrush(fill_color)
        painter.setPen(QPen(outline_color, 2, Qt.DotLine))
        painter.drawEllipse(self.highlight_pin.x() - 3, self.highlight_pin.y() - 3, 6, 6)

    def paintEvent(self, *args):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        r = self.rect()
        painter.fillRect(r, Qt.white)

        for element in self.elements:
            painter.translate(element.bounding_box.topLeft())
            element.paint(painter)
            painter.translate(-element.bounding_box.topLeft())
            self.update_pins(element)

        self._draw_wires(painter, self.wires)
        self._draw_wires(painter, self.buses, 4)

        if self.highlight_pin is not None:
            self._highlight_pin(painter)

        painter.setPen(QPen(Qt.red, 1, Qt.DashLine))
        painter.setBrush(Qt.transparent)
        for element in self.selected_elements:
            bb = element.bounding_box
            bb = bb.marginsAdded(QMargins(2, 2, 1, 1))
            painter.drawRect(bb)

        if self.select_rect is not None:
            painter.setBrush(QColor(0, 0, 255, 64))
            painter.setPen(QColor(0, 0, 255, 128))
            painter.drawRect(self.select_rect)

        if self.wiring_mode:
            painter.setPen(QPen(Qt.red, 1, Qt.PenStyle.DotLine))
            for line in self.guidelines:
                painter.drawLine(line)

            if self._ghost_wire is not None:
                self._draw_wire(painter, self._ghost_wire, True)
                if self.is_bus:
                    self._draw_wire(painter, self._ghost_wire, True, 4)


    def _pick(self, p):
        for element in self.elements:
            if element.bounding_box.contains(p):
                return element
        return None


    def get_selected_pin(self, pos):
        for vals, element in zip(self.pins.values(), self.pins):
            for pin,i in zip(vals,range(len(vals))):
                if pin.x()-8 <= pos.x() and pin.y()-8 <= pos.y():
                    if pin.x()+8 >= pos.x() and pin.y()+8 >= pos.y():
                        return pin, element, i
        return None, None, None


    def mousePressEvent(self, e):
        selected_pin, in_element, pin_index = self.get_selected_pin(e.pos())
        if selected_pin:
            self.wiring_mode = True
            if not self._wire_start:
                if selected_pin is not None:
                    if in_element.pins[pin_index].size > 1:
                        self.is_bus = True
                        self.bus_size = in_element.pins[pin_index].size
                    else:
                        self.is_bus = False
                    self._wire_start = True
                    self._ghost_wire = [selected_pin]
                    self.start_element = in_element
                    self.pin_index = pin_index
                    self.highlight_pin = None
                    selected_pin = None
        else:
            self.grabbed_element = self._pick(e.pos())
            if self.grabbed_element is not None:
                self.grab_offset = self.grabbed_element.bounding_box.topLeft() - e.pos()
            else:
                self.select_rect = QRect(e.pos(), QSize(0, 0))

    def mouseMoveEvent(self, e):
        if self.wiring_mode:
            if self._ghost_wire is not None:
                if len(self._ghost_wire) == 1:
                    self._ghost_wire.append(QPoint(e.pos().x(), self._ghost_wire[-1].y()))
                    self._ghost_wire.append(e.pos())
                if len(self._ghost_wire) <= 3:
                    mode = self.start_element.oriantation
                    if mode == 0 or mode == 2:    
                        self._ghost_wire[-2] = QPoint(e.pos().x(), self._ghost_wire[-3].y())
                        self._ghost_wire[-1] = QPoint(self._ghost_wire[-2].x(), e.pos().y())
                else:
                    if self._ghost_wire[-4].x() == self._ghost_wire[-3].x():
                        self._ghost_wire[-2] = QPoint(e.pos().x(), self._ghost_wire[-3].y())
                        self._ghost_wire[-1] = e.pos()
                    elif self._ghost_wire[-4].y() == self._ghost_wire[-3].y():
                        self._ghost_wire[-2] = QPoint(self._ghost_wire[-3].x(), e.pos().y())
                        self._ghost_wire[-1] = e.pos()
            else:
                self._ghost_wire = None
            self.highlight_pin, _, _ = self.get_selected_pin(e.pos())
            self.update()
        else:
            if self.grabbed_element is not None:
                self.grabbed_element.bounding_box.moveTopLeft(
                    e.pos() + self.grab_offset)
                # print(e.pos() + self.grab_offset,"qqq")
                self.continuous_update(self.wires)
                self.continuous_update(self.buses)

                self.moved = True
                self.update()
            elif self.select_rect is not None:
                self.select_rect.setBottomRight(e.pos())
                if self.select_rect.size() != QSize(0, 0):
                    self.selected_elements = list()
                    for element in self.elements:
                        if self.select_rect.contains(element.bounding_box):
                            self.selected_elements.append(element)
                self.update()
            self.highlight_pin, _, _ = self.get_selected_pin(e.pos())
            self.update()

    def mouseReleaseEvent(self, e):
        if self.wiring_mode:
            if e.button() == Qt.LeftButton:
                if self._ghost_wire is not None:
                    wire_end, out_element, pin_index = self.get_selected_pin(e.pos())
                    if wire_end is not None:
                        if self.start_element != out_element:
                            conn = connection(self.start_element, self.pin_index, out_element, pin_index)
                            if not self.is_bus:
                                if out_element.pins[pin_index].size == 1:
                                    self.wires.append(WireElement(conn, self._ghost_wire))
                            else:
                                if out_element.pins[pin_index].size == self.bus_size:
                                    self.buses.append(BusElement(conn, self._ghost_wire, self.bus_size))
                                self.is_bus = False
                                self.bus_size = None
                        self._ghost_wire = None
                        self._wire_start = False
                        wire_end = None
                        self.wiring_mode = False
                        self.highlight_pin = None
                    else:
                        if self._ghost_wire is not None:
                            self._ghost_wire.append(e.pos())
                            self._ghost_wire.append(e.pos())
                
                    self.update()
        else:
            moved = self.moved

            if self.grabbed_element is not None:
                self.grabbed_element = None
                self.moved = False

            if not moved:
                self.selected_elements = list()
                if self.select_rect is not None and self.select_rect.size() != QSize(0, 0):
                    for element in self.elements:
                        if self.select_rect.contains(element.bounding_box):
                            self.selected_elements.append(element)
                else:
                    for element in self.elements:
                        bb = element.bounding_box
                        if bb.contains(e.pos()):
                            self.selected_elements.append(element)
                            break
                self.select_rect = None
                self.update()


    def resizeEvent(self, e):
        super().resizeEvent(e)
        # self._build_guidelines()
        self.update()


    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Escape:
            if self.wiring_mode:
                self.wiring_mode = False
                self._ghost_wire = None
                self._wire_start = False
                self.update()
        elif e.key() == Qt.Key_Delete:
            for element in self.selected_elements:
                self.elements.remove(element)
                self.update()
        elif e.key() == Qt.Key_Backspace:
            del self._ghost_wire[-1]
        
    # def keyPressEvent(self, e):
        elif e.key() == Qt.Key_Plus and e.modifiers() & Qt.ControlModifier:
            for element in self.selected_elements:
                element.resize(0)
                self.update()
        elif e.key() == Qt.Key_Minus and e.modifiers() & Qt.ControlModifier:
            for element in self.selected_elements:
                element.resize(1)
                self.update()


    def continuous_update(self, netlist):
        for wire in netlist:
            if wire.connection.In_module == self.grabbed_element:
                pin = wire.connection.In_pin
                st_pnt = wire.points[-1]
                dy_pnt = self.pins[self.grabbed_element][pin]
                update_wire(dy_pnt, st_pnt, wire)

            if wire.connection.Out_module == self.grabbed_element:
                pin = wire.connection.Out_pin
                st_pnt = wire.points[0]
                dy_pnt = self.pins[self.grabbed_element][pin]
                update_wire(st_pnt, dy_pnt, wire)

    