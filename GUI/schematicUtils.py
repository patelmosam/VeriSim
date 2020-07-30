from PySide2.QtWidgets import QWidget, QOpenGLWidget
from PySide2.QtCore import QRect, QSize, Qt, QPoint, QMargins, QLine
from PySide2.QtGui import QColor, QPen, QPainter, QMouseEvent, QPolygon, QPainterPath, QVector2D, QPainterPathStroker


def update_wire(dy_pnt, st_pnt, wire):

    wire.points = []
    wire.points.append(dy_pnt)
    wire.points.append(QPoint(dy_pnt.x()+abs(st_pnt.x()-dy_pnt.x())/2,dy_pnt.y()))
    wire.points.append(QPoint(dy_pnt.x()+abs(st_pnt.x()-dy_pnt.x())/2,st_pnt.y()))
    wire.points.append(st_pnt)

    # for i in range(len(wire.points)-1):
    #     rect = make_line_rect([wire.points[i], wire.points[i+1]])
        # is_intetsect, bb = is_interseted(elements, rect, wire.connection.In_module, wire.connection.Out_module)
        # print(is_intetsect)
        # if is_intetsect:
        #     x, y, h, w = bb.x(), bb.y(), bb.height(), bb.width()
        #     p1, p2, p3, p4 = QPoint(x,y), QPoint(x+w,y), QPoint(x,y+h), QPoint(x+w,y+h)

            # _update_wire2(i, i+1, wire, p1, p2, p3, p4)
            # _update_wire2(i+1, i, wire, p1, p2, p3, p4)

def make_line_rect(line):
    hight = abs(line[0].y() - line[1].y()) 
    width = abs(line[0].x() - line[1].x()) 
    return QRect(QPoint(line[0]),QSize(width, hight))

def is_interseted(elements, rect, in_module, out_module):
    res = False
    bb = None
    for element in elements:
        if element != in_module and element != out_module:
            if element.bounding_box.intersects(rect):
                res = True
                bb = element.bounding_box
                break
    return res, bb

def _update_wire2(i, j, wire, p1, p2, p3, p4):
    if wire.points[i].x()-wire.points[j].x() == 0:
        c = (p3.x() + p4.x())/2 
        if p1.x() <= wire.points[i].x() <= c:
            np1 = QPoint(wire.points[i].x(), p1.y()-10)
            np2 = QPoint(p1.x()-10, p1.y()-10)
            np3 = QPoint(p1.x()-10, p3.y()+10)
            np4 = QPoint(wire.points[i].x(), p3.y()+10)
        else:
            np1 = QPoint(wire.points[i].x(), p2.y()-10)
            np2 = QPoint(p2.x()+10, p2.y()-10)
            np3 = QPoint(p2.x()+10, p4.y()+10)
            np4 = QPoint(wire.points[i].x(), p4.y()+10)

        for np in [np4,np3,np2,np1]:
            wire.points.insert(j,np)
    else:
        c = (p1.y() + p3.y())/2 
        if p1.y() <= wire.points[i].y() <= c:
            np1 = QPoint(p1.x()-10, wire.points[i].y())
            np2 = QPoint(p1.x()-10, p1.y()-10)
            np3 = QPoint(p2.x()+10, p1.y()-10)
            np4 = QPoint(p2.x()+10, wire.points[i].y())
        else:
            np1 = QPoint(p3.x()-10, wire.points[i].y())
            np2 = QPoint(p3.x()-10, p3.y()+10)
            np3 = QPoint(p4.x()+10, p3.y()+10)
            np4 = QPoint(p4.x()+10, wire.points[i].y())

        for np in [np4,np3,np2,np1]:
            wire.points.insert(j,np)