import typing

from PyQt5.QtCore import QSizeF, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsRectItem, QWidget

from swikv4.pages.swik_page import SwikPage


class NumberBanner(QGraphicsRectItem):
    def __init__(self, parent, number):
        super().__init__(parent)
        # self.setBrush(QColor(255, 0, 0, 100))
        self.number = number
        self.setFlags(self.ItemIgnoresTransformations)

    def paint(self, painter, option, widget=...):
        super().paint(painter, option, widget)
        font = QFont("Arial", 18)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, str(self.number))


class SwikMiniaturePage(SwikPage):
    def __init__(self, index, size, ratio, view, renderer):
        super().__init__(index, size, ratio, view, renderer)
        self.number_banner = NumberBanner(self, index + 1)
        # self.number_banner.setRect(0, size.height() + 10, size.width(), 100)

    def get_original_size(self):
        return self.original_size + QSizeF(0, 50)

    # def get_zoomed_size(self):
    #    return QSizeF(self.original_size.width() * self.ratio, (self.original_size.height() + 50) * self.ratio)

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        super().paint(painter, option, widget)
        # constant_height = self.ratio * 100
        self.number_banner.setRect(0, 0, self.rect().width() * self.ratio, 30)
        self.number_banner.setPos(0, self.rect().height())

    def set_index(self, number):
        super().set_index(number)
        self.number_banner.number = number + 1
        self.number_banner.update()
