from PyQt5.QtWidgets import QGraphicsWidget
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtGui

class QGraphicsRectWidget(QGraphicsWidget):

    def __init__(self, parent=None):
        super(QGraphicsRectWidget, self).__init__(parent)

    def paint(self, painter, option, widget):
        painter.fillRect(self.rect(), QtGui.QColor(205, 133, 63))
        painter.drawText(self.rect().center(), self._text)

    @pyqtProperty(str)
    def text(self, text):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
