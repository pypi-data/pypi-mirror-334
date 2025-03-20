from PyQt5.QtWidgets import QComboBox

from swikv4.resources import resources  # noqa
from swikv4.toolbars.swik_toolbar import SwikToolBar


class DynamicComboBox(QComboBox):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.options = options
        self.addItems(options)

    def items(self):
        return self.options

    def showPopup(self):
        self.blockSignals(True)
        self.clear()
        self.addItems(self.options)
        self.blockSignals(False)
        super().showPopup()


class SwikZoomToolbar(SwikToolBar):
    def __init__(self, view, toolbar=None):
        super(SwikZoomToolbar, self).__init__(view, toolbar)
        self.view = view
        self.layout_manager = view.get_layout_manager()
        self.layout_manager.layout_mode_changed.connect(self.layout_mode_changed)
        self.zoom_combobox = DynamicComboBox(
            ["10%", "25%", "50%", "75%", "100%", "125%", "150%", "200%", "400%", "Fit Width"])
        self.zoom_combobox.addItems(["10%", "100%"])
        self.zoom_combobox.setEditable(True)
        self.zoom_in_btn = self.add_action("Zoom out", self.zoom_out, ":/icons/zoom-out.png")
        self.toolbar().addWidget(self.zoom_combobox)
        self.zoom_out_btn = self.add_action("Zoom In", self.zoom_in, ":/icons/zoom-in.png")
        self.layout_mode_changed(self.layout_manager.layout_mode, self.layout_manager.layout_ratio)
        self.zoom_combobox.currentIndexChanged.connect(self.zoom_combobox_changed)

    def layout_mode_changed(self, mode, ratio):
        self.zoom_combobox.blockSignals(True)
        if mode == 0:
            self.zoom_combobox.setCurrentIndex(9)
            self.zoom_combobox.setEditable(False)
        else:
            self.zoom_combobox.setEditable(True)
            goal_zoom = f"{int(ratio * 100)}%"

            # Bug workaround: if we set a currentText that is in the list the
            # currentIndexChanged signal is emitted even with blockSignals(True)
            if self.zoom_combobox.findText(goal_zoom) >= 0:
                self.zoom_combobox.setCurrentIndex(self.zoom_combobox.findText(goal_zoom))
            else:
                self.zoom_combobox.setCurrentText(goal_zoom)

            # self.zoom_combobox.setCurrentText()
        self.zoom_combobox.blockSignals(False)

    def zoom_combobox_changed(self, index):
        if index == 9:
            self.layout_manager.set_mode(0)
        else:
            self.layout_manager.set_mode(1, int(self.zoom_combobox.currentText().replace("%", "")) / 100)

    def zoom_in(self):
        self.view.zoom(self.view.get_ratio() * 1.1)

    def zoom_out(self):
        self.view.zoom(self.view.get_ratio() * 0.9)
