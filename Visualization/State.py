from PyQt5.QtCore import (QAbstractTransition, QEvent, QRect, QState)
# from PyQt5 import QtGui

class StateSwitchEvent(QEvent):
    StateSwitchType = QEvent.User + 256

    def __init__(self, rand=0):
        super(StateSwitchEvent, self).__init__(StateSwitchEvent.StateSwitchType)

        self.m_rand = rand

    def rand(self):
        return self.m_rand

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
                    item.assignProperty(plates[number - 1], 'text', text)
                width += tile_size
            height += tile_size
        result.append(item)

    return result
