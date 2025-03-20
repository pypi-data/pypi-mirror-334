from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit, QLabel

from swikv4.toolbars.swik_toolbar import SwikToolBar


class SwikPageNavigationToolbar(SwikToolBar):
    def __init__(self, view, renderer, toolbar=None):
        super(SwikPageNavigationToolbar, self).__init__(view, toolbar)
        self.view = view
        self.renderer = renderer

        self.page_text = QLineEdit()
        self.page_text.setMaximumWidth(40)
        self.page_text.setAlignment(Qt.AlignRight)
        self.page_max_text = QLabel()
        self.page_text.returnPressed.connect(self.page_text_changed)

        self.prev_page_btn = self.add_action("-", self.prev_page, ":/icons/left.png")
        self.toolbar().addWidget(self.page_text)
        self.toolbar().addWidget(self.page_max_text)
        self.next_page_btn = self.add_action("+", self.next_page, ":/icons/right.png")

        self.view.page_number_changed.connect(self.page_number_changed)
        self.page_text.setValidator(QIntValidator(1, 5000))
        self.enable_interactions(False)

    def page_number_changed(self, number):
        self.page_text.blockSignals(True)
        self.page_text.setText(str(number + 1))
        self.page_max_text.setText("/" + str(self.renderer.get_document_length()))
        self.page_text.blockSignals(False)
        self.enable_interactions(True)

    def enable_interactions(self, value):
        self.page_text.setEnabled(value)
        self.prev_page_btn.setEnabled(value)
        self.next_page_btn.setEnabled(value)

    def page_text_changed(self):
        text = self.page_text.text()
        # if self.page_text.validator().validate(text, 0):
        page_number = int(text) - 1
        self.view.move_to_page(page_number)

    def next_page(self):
        self.view.move_to_page(self.view.get_current_page_number() + 1)

    def prev_page(self):
        self.view.move_to_page(self.view.get_current_page_number() - 1)
