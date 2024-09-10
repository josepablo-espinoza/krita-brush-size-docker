from krita import *
from PyQt5 import QtCore

class BrushSizeDockerExtension(Extension):

    SIGNAL_CYCLE = QtCore.pyqtSignal()

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        pass
        
    def createActions(self, window):
        action = window.createAction("cycleBrushSize", "Next brush size", "tools/scripts")
        action.triggered.connect(self.cycleBrushSize)

    def cycleBrushSize(self):
        self.SIGNAL_CYCLE.emit()