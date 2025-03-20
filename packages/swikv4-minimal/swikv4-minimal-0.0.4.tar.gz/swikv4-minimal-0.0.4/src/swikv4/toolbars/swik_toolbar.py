from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar


class SwikToolBar(QObject):

    def __init__(self, view, tb=None):
        super().__init__()
        self.view = view
        self.tb = tb if tb is not None else QToolBar()
        self.widgets = []

    def attach(self, toolbar):
        pass

    def toolbar(self):
        return self.tb

    def add_action(self, text, callback, icon=None):
        action = self.tb.addAction(text, callback)
        action.setIcon(QIcon(icon))
        self.widgets.append(action)
        return action

    def add_widget(self, widget):
        action = self.tb.addWidget(widget)
        self.widgets.append(action)

    def hide(self):
        for w in self.widgets:
            w.setVisible(False)

    def show(self):
        for w in self.widgets:
            w.setVisible(True)
