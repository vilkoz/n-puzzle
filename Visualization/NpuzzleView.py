import sys

from Visualization.RectWidget import QGraphicsRectWidget
from Visualization.State import (createGeometryStates, StateSwitcher, StateSwitchTransition, StateSwitchEvent)
from PyQt5 import QtGui
from PyQt5.QtCore import (QParallelAnimationGroup, QSequentialAnimationGroup, QPropertyAnimation,
							QEasingCurve, Qt, QStateMachine, QState, QTimer, qsrand, QTime)
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView)

class NpuzzleView:
    def __init__(self, states):
        self.states = states
        self.size = len(states[0])
        self.tile_size = 150
        print ("Scene size = {}".format(self.size))
    
    def printState(self, state):
        s = ""
        for row in state:
            for item in row:
                s += str(item) + " "
            s += "\n"
        print(s, end="")

    def display(self):
        for i, state in enumerate(self.states):
            print("step number %d: " % (i))
            self.printState(state)

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

        returnCode = app.exec_()

        del machine
        del window
        del scene
        del app
        
        sys.exit(returnCode)
