import sys

from PyQt5 import QtGui
from PyQt5.QtCore import (QAbstractTransition, QEasingCurve, QEvent,
        QParallelAnimationGroup, QPropertyAnimation, qrand, QRect,
        QSequentialAnimationGroup, qsrand, QState, QStateMachine, Qt, QTime,
        QTimer)
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView,
        QGraphicsWidget, QLabel)


class StateSwitchEvent(QEvent):
    StateSwitchType = QEvent.User + 256

    def __init__(self, rand=0):
        super(StateSwitchEvent, self).__init__(StateSwitchEvent.StateSwitchType)

        self.m_rand = rand

    def rand(self):
        return self.m_rand

class QGraphicsRectWidget(QGraphicsWidget):
    def paint(self, painter, option, widget):
        painter.fillRect(self.rect(), QtGui.QColor(205, 133, 63))
        painter.drawText(self.rect().center(), self.windowTitle())

class StateSwitchTransition(QAbstractTransition):
    def __init__(self, rand):
        super(StateSwitchTransition, self).__init__()

        self.m_rand = rand

    def eventTest(self, event):
        return (event.type() == StateSwitchEvent.StateSwitchType and
                event.rand() == self.m_rand)

    def onTransition(self, event):
        pass


class StateSwitcher(QState):
    def __init__(self, machine):
        super(StateSwitcher, self).__init__(machine)

        self.stateCount = 0
        self.lastViewIndex = 0

    def onEntry(self, event):
        self.machine().postEvent(StateSwitchEvent(self.lastViewIndex + 1))
        self.lastViewIndex += 1
        if self.lastViewIndex == self.stateCount:
            self.lastViewIndex = 0

    def onExit(self, event):
        pass

    def addState(self, state, animation):
        self.stateCount += 1
        trans = StateSwitchTransition(self.stateCount)
        trans.setTargetState(state)
        self.addTransition(trans)
        trans.addAnimation(animation)

def createGeometryStates(states, plates, parent, tile_size):
    result = []

    for state in states:
        item = QState(parent)
        
        height = 1
        for row in state:
            width = 1
            for number in row:
                if number != 0:
                    rect = QRect(width, height, tile_size - 2, tile_size - 2)
                    text = str(number)
                    # how to put another item to rect?
                    item.assignProperty(plates[number - 1], 'geometry', rect)
                    item.assignProperty(plates[number - 1], 'windowTitle', text)
                width += tile_size
            height += tile_size
        result.append(item)

    return result

class NpuzzleView:
    def __init__(self, states):
        self.states = states
        self.size = len(states[0])
        self.tile_size = 150
        print ("Scene size = {}".format(self.size))
    
    def print_state(self, state):
        s = ""
        for row in state:
            for item in row:
                s += str(item) + " "
            s += "\n"
        print(s, end="")

    def display(self):
        for i, state in enumerate(self.states):
            print("step number %d: " % (i))
            self.print_state(state)

        app = QApplication(sys.argv)

        scene = QGraphicsScene(0, 0, self.size * self.tile_size, self.size * self.tile_size)
        scene.setBackgroundBrush(QtGui.QColor(255, 255, 224))

        plates = []
        animationGroup = QParallelAnimationGroup()
        for i in range(self.size * self.size - 1):
            plates.append(QGraphicsRectWidget())
            scene.addItem(plates[i])
            subGroup = QSequentialAnimationGroup(animationGroup)
            subGroup.addPause(100)
            anim = QPropertyAnimation(plates[i], b'geometry')
            anim.setDuration(1000)
            anim.setEasingCurve(QEasingCurve.OutElastic)
            subGroup.addAnimation(anim)

        window = QGraphicsView(scene)
        window.setWindowTitle('n-puzzle')
        window.setFrameStyle(0)
        window.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        window.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        machine = QStateMachine()

        group = QState()
        timer = QTimer()
        timer.setInterval(325)
        timer.setSingleShot(True)
        group.entered.connect(timer.start)

        geometryState = createGeometryStates(self.states, plates, group, self.tile_size)

        group.setInitialState(geometryState[0])

        stateSwitcher = StateSwitcher(machine)
        group.addTransition(timer.timeout, stateSwitcher)
        for item in geometryState:
            stateSwitcher.addState(item, animationGroup)

        machine.addState(group)
        machine.setInitialState(group)
        machine.start()

        window.resize(self.size * self.tile_size, self.size * self.tile_size)
        window.show()

        qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))

        app.exec_()
