from PySide2.QtWidgets import QWidget, QOpenGLWidget
from PySide2.QtCore import QRect, QSize, Qt, QPoint, QMargins, QLine
from PySide2.QtGui import QColor, QPen, QPainter, QMouseEvent, QPolygon, QPainterPath, QVector2D, QPainterPathStroker


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
        self.pins = dict()

        self.guidepoints = list() # unused
        self.guidelines = list()
        self._ghost_wire = None
        self.wiring_mode = False
        self.closest_point = None

        self._wire_start = False
        self.wire_tip = None

        self.select_rect = None

        self.selected_elements = list()
        self.moved = False
        self.grabbed_element = None
        self.grab_offset = None
        
        self.start_element = None
        self.end_element = None

    def get_pins(self):
        for element in self.elements:
            self.pins[element] = []
            for pin in element.pins():
                p = pin.position + element.bounding_box.topLeft()
                self.pins[element].append(p)

    def update_pins(self, element):
        self.pins[element] = []
        for pin in element.pins():
            p = pin.position + element.bounding_box.topLeft()
            self.pins[element].append(p)

    def _draw_wire(self, painter, line, ghost):
        # path = None
        # path = QPainterPath(line[0])
        # for point in line[1:-1]:
        #     path.lineTo(point)
        # if line[-1] is not None:
        #     path.lineTo(line[-1])

        fill_color = QColor(0, 0, 0)
        outline_color = QColor(0, 0, 0)

        if ghost:
            fill_color.setAlphaF(0.5)
            outline_color.setAlphaF(0.5)

        painter.setPen(QPen(outline_color, 2))
        # painter.fillPath(stroke, fill_color)
        for i in range(len(line)-1):
            painter.drawLine(line[i],line[i+1])

    def _draw_wires(self, painter):
        # path = QPainterPath()
        # # print(len(self.wires))
        # for wire in self.wires:
        #     path = QPainterPath(wire[0])
        #     for point in wire:
        #         path.lineTo(point)

            p = QPen(Qt.red, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)

            # stroker = QPainterPathStroker(p)
            # stroke = stroker.createStroke(path).simplified()

            fill_color = QColor(255, 0, 0)
            outline_color = QColor(255, 0, 0)

            painter.setPen(QPen(outline_color, 2))
            # painter.fillPath(stroke, fill_color)
            # painter.drawPath(path)
            for wire in self.wires:
                for i in range(len(wire)-1):
                    painter.drawLine(wire[i],wire[i+1])

    def _draw_pin(self, painter, point):
        fill_color = QColor(255, 255, 255)
        outline_color = QColor(0, 0, 0)
        painter.setBrush(fill_color)
        painter.setPen(QPen(outline_color, 2))
        painter.drawEllipse(point.x() - 4, point.y() - 4, 8, 8)

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

        self._draw_wires(painter)

        for element in self.elements:
            for pin in element.pins():
                p = pin.position + element.bounding_box.topLeft()
                self._draw_pin(painter, p)

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

            if self.closest_point is not None:
                p = self.closest_point
                painter.drawEllipse(p.x() - 4, p.y() - 4, 8, 8)

    def _pick(self, p):
        for element in self.elements:
            if element.bounding_box.contains(p):
                return element
        return None

    # def _closest_guideline_point(self, point):
    #     currd = None
    #     closest = None
    #     is_junction = False
    #     for element in self.elements:
    #         for pin in element.pins():
    #             p = pin.position + element.bounding_box.topLeft()
    #             d = QVector2D(p - point).lengthSquared()
    #             if (currd is None or d < currd) and d < 2500:
    #                 currd = d
    #                 closest = p
    #                 is_junction = True
    #     for wire in self.wires:
    #         for p in (wire.p1(), wire.p2()):
    #             d = QVector2D(p - point).lengthSquared()
    #             if (currd is None or d < currd) and d < 2500:
    #                 currd = d
    #                 closest = p
    #                 is_junction = True
    #     for line in self.guidelines:
    #         p = _closest_point(line, point)
    #         d = QVector2D(p - point).lengthSquared()
    #         if not _is_point_on_line(line, p):
    #             continue
    #         if self._wire_start is not None:
    #             delta = p - self._wire_start
    #             if delta.x() != 0 and delta.y() != 0:
    #                 continue
    #         if (currd is None or ((not is_junction and d < currd) or (is_junction and abs(d - currd) > 100))) and d < 2500:
    #             currd = d
    #             closest = p
    #     return closest

    # def _closest_assist_point(self, point):
    #     gp = self._closest_guideline_point(point)
    #     return gp
    

    def get_selected_pin(self, pos):
        for vals, element in zip(self.pins.values(), self.pins):
            for pin in vals:
                if pin.x()-8 <= pos.x() and pin.y()-8 <= pos.y():
                    if pin.x()+8 >= pos.x() and pin.y()+8 >= pos.y():
                        return pin, element
        # print(_type)
        
        return None, None

    def check_wire_tip(self, pos):
        if self.wire_tip is not None:
            if self.wire_tip.x()-8 <= pos.x() and self.wire_tip.y()-8 <= pos.y():
                if self.wire_tip.x()+8 >= pos.x() and self.wire_tip.y()+8 >= pos.y():
                    return self.wire_tip
        return None 

    def mousePressEvent(self, e):
        if self.wiring_mode:
            selected_pin, pin_element = self.get_selected_pin(e.pos())
            if not self._wire_start:
                if selected_pin is not None:
                    self._wire_start = True
                    self.start_element = pin_element
                    self._ghost_wire = [selected_pin]
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
                    # print(self._ghost_wire)
            else:
                # print("not")
                self._ghost_wire = None
            self.update()
        else:
            if self.grabbed_element is not None:
                self.grabbed_element.bounding_box.moveTopLeft(
                    e.pos() + self.grab_offset)
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

    def mouseReleaseEvent(self, e):
        if self.wiring_mode:
            if e.button() == Qt.LeftButton:
                if self._ghost_wire is not None:
                    wire_end, pin_element = self.get_selected_pin(e.pos())
                    if wire_end is not None:
                        # print("ghost ",self._ghost_wire)
                        # wire_mid = QPoint(self._wire_start.x(), wire_end.y())
                        self.wires.append(self._ghost_wire)
                        self._ghost_wire = None
                        self._wire_start = False
                        wire_end = None
                        # for i in self.wires:
                            # print("wire ",len(i))
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

    # def _build_guidelines(self):
    #     self.guidelines = list()
    #     for element in self.elements:
    #         for pin in element.pins():
    #             p = pin.position + element.bounding_box.topLeft()
    #             if pin.direction.y() == 0:
    #                 if pin.direction.x() > 0:
    #                     self.guidelines.append(
    #                         QLine(p.x(), p.y(), self.rect().width(), p.y()))
    #                 else:
    #                     self.guidelines.append(
    #                         QLine(p.x(), p.y(), 0, p.y()))
    #                 self.guidelines.append(
    #                     QLine(p.x(), 0, p.x(), self.rect().height()))
    #             else:
    #                 if pin.direction.y() > 0:
    #                     self.guidelines.append(
    #                         QLine(p.x(), p.y(), p.x(), self.rect().height()))
    #                 else:
    #                     self.guidelines.append(
    #                         QLine(p.x(), p.y(), p.x(), 0))
    #                 self.guidelines.append(
    #                     QLine(0, p.y(), self.rect().width(), p.y()))
    #     for wire in self.wires:
    #         for p in (wire.p1(), wire.p2()):
    #             self.guidelines.append(
    #                 QLine(0, p.y(), self.rect().width(), p.y()))
    #             self.guidelines.append(
    #                 QLine(p.x(), 0, p.x(), self.rect().height()))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        # self._build_guidelines()
        self.update()

    def _leave_wiring_mode(self):
        self.wiring_mode = False

    def _enter_wiring_mode(self):
        self.wiring_mode = True
        self._ghost_wire = None
        self.closest_point = None
        self.selected_elements = list()
        # self._build_guidelines()

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_W:
            if not self.wiring_mode:
                self._enter_wiring_mode()
                self.wiring_mode = True
            else:
                self._leave_wiring_mode()
                self.wiring_mode = False
            self.update()
        elif e.key() == Qt.Key_Escape:
            if self.wiring_mode:
                self._leave_wiring_mode()
                self.wiring_mode = False
                self.update()
        elif e.key() == Qt.Key_Delete:
            for element in self.selected_elements:
                self.elements.remove(element)
                self.update()
        elif e.key() == Qt.Key_Backspace:
            del self._ghost_wire[-1]
