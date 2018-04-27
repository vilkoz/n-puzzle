import sys

from PyQt5.QtCore import (QAbstractTransition, QEasingCurve, QEvent,
        QParallelAnimationGroup, QPropertyAnimation, qrand, QRect,
        QSequentialAnimationGroup, qsrand, QState, QStateMachine, Qt, QTime,
        QTimer)
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView,
        QGraphicsWidget)


class StateSwitchEvent(QEvent):
    StateSwitchType = QEvent.User + 256

    def __init__(self, rand=0):
        super(StateSwitchEvent, self).__init__(StateSwitchEvent.StateSwitchType)

        self.m_rand = rand

    def rand(self):
        return self.m_rand


class QGraphicsRectWidget(QGraphicsWidget):
    def paint(self, painter, option, widget):
        painter.fillRect(self.rect(), Qt.blue)


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

        self.m_stateCount = 0
        self.m_lastIndex = 0

    def onEntry(self, event):
        n = qrand() % self.m_stateCount + 1
        while n == self.m_lastIndex:
            n = qrand() % self.m_stateCount + 1

        self.m_lastIndex = n
        self.machine().postEvent(StateSwitchEvent(n))

    def onExit(self, event):
        pass

    def addState(self, state, animation):
        self.m_stateCount += 1
        trans = StateSwitchTransition(self.m_stateCount)
        trans.setTargetState(state)
        self.addTransition(trans)
        trans.addAnimation(animation)

def createGeometryStates(states, plates, parent):
# def createGeometryState(w1, rect1, w2, rect2, w3, rect3, w4, rect4, parent):
    result = []

    item = QState(parent)

    item.assignProperty(plates[0], 'geometry', QRect(0, 0, 49, 49))
    item.assignProperty(plates[1], 'geometry', QRect(50, 0, 49, 49))
    item.assignProperty(plates[2], 'geometry', QRect(100, 0, 49, 49))

    result.append(item)

    item2 = QState(parent)

    item2.assignProperty(plates[0], 'geometry', QRect(150, 0, 49, 49))
    item2.assignProperty(plates[1], 'geometry', QRect(150, 50, 49, 49))
    item2.assignProperty(plates[2], 'geometry', QRect(150, 100, 49, 49))

    result.append(item2)

    return result

class NpuzzleView:
    def __init__(self, states):
        self.states = states
        self.size = len(states[0])
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

        scene = QGraphicsScene(0, 0, self.size * 50, self.size * 50)
        scene.setBackgroundBrush(Qt.white)

        plates = []
        for i in range(self.size * self.size - 1):
            plates.append(QGraphicsRectWidget())
            scene.addItem(plates[i])

        # button1 = plates[0]
        # button2 = plates[1]
        # button3 = plates[2]
        # button4 = plates[3]

        window = QGraphicsView(scene)
        window.setFrameStyle(0)
        window.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        window.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        machine = QStateMachine()

        group = QState()
        timer = QTimer()
        timer.setInterval(1250)
        timer.setSingleShot(True)
        group.entered.connect(timer.start)

        geometryState = createGeometryStates(self.states, plates, group)
        # state1 = createGeometryState(button1, QRect(100, 0, 50, 50), button2,
        #         QRect(150, 0, 50, 50), button3, QRect(200, 0, 50, 50), button4,
        #         QRect(250, 0, 50, 50), group)

        # state2 = createGeometryState(button1, QRect(250, 100, 50, 50), button2,
        #         QRect(250, 150, 50, 50), button3, QRect(250, 200, 50, 50), button4,
        #         QRect(250, 250, 50, 50), group)

        # state3 = createGeometryState(button1, QRect(150, 250, 50, 50), button2,
        #         QRect(100, 250, 50, 50), button3, QRect(50, 250, 50, 50), button4,
        #         QRect(0, 250, 50, 50), group)

        # state4 = createGeometryState(button1, QRect(0, 150, 50, 50), button2,
        #         QRect(0, 100, 50, 50), button3, QRect(0, 50, 50, 50), button4,
        #         QRect(0, 0, 50, 50), group)

        # state5 = createGeometryState(button1, QRect(100, 100, 50, 50), button2,
        #         QRect(150, 100, 50, 50), button3, QRect(100, 150, 50, 50), button4,
        #         QRect(150, 150, 50, 50), group)

        # state6 = createGeometryState(button1, QRect(50, 50, 50, 50), button2,
        #         QRect(200, 50, 50, 50), button3, QRect(50, 200, 50, 50), button4,
        #         QRect(200, 200, 50, 50), group)

        # state7 = createGeometryState(button1, QRect(0, 0, 50, 50), button2,
        #         QRect(250, 0, 50, 50), button3, QRect(0, 250, 50, 50), button4,
        #         QRect(250, 250, 50, 50), group)

        group.setInitialState(geometryState[0])

        animationGroup = QParallelAnimationGroup()
        anim = QPropertyAnimation(plates[3], b'geometry')
        anim.setDuration(1000)
        anim.setEasingCurve(QEasingCurve.OutElastic)
        animationGroup.addAnimation(anim)

        subGroup = QSequentialAnimationGroup(animationGroup)
        subGroup.addPause(100)
        anim = QPropertyAnimation(plates[2], b'geometry')
        anim.setDuration(1000)
        anim.setEasingCurve(QEasingCurve.OutElastic)
        subGroup.addAnimation(anim)

        subGroup = QSequentialAnimationGroup(animationGroup)
        subGroup.addPause(150)
        anim = QPropertyAnimation(plates[1], b'geometry')
        anim.setDuration(1000)
        anim.setEasingCurve(QEasingCurve.OutElastic)
        subGroup.addAnimation(anim)

        subGroup = QSequentialAnimationGroup(animationGroup)
        subGroup.addPause(200)
        anim = QPropertyAnimation(plates[0], b'geometry')
        anim.setDuration(1000)
        anim.setEasingCurve(QEasingCurve.OutElastic)
        subGroup.addAnimation(anim)

        stateSwitcher = StateSwitcher(machine)
        group.addTransition(timer.timeout, stateSwitcher)
        stateSwitcher.addState(geometryState[0], animationGroup)
        stateSwitcher.addState(geometryState[1], animationGroup)
        # stateSwitcher.addState(state3, animationGroup)
        # stateSwitcher.addState(state4, animationGroup)
        # stateSwitcher.addState(state5, animationGroup)
        # stateSwitcher.addState(state6, animationGroup)
        # stateSwitcher.addState(state7, animationGroup)

        machine.addState(group)
        machine.setInitialState(group)
        machine.start()

        window.resize(self.size * 50, self.size * 50)
        window.show()

        qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))

        app.exec_()
