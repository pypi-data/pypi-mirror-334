import typing

from PyQt5.QtCore import QRectF, QTimer, QRect
from PyQt5.QtGui import QTransform, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsRectItem


class SwikPage(QGraphicsRectItem):

    def __init__(self, index, size, ratio, view: QGraphicsView, renderer):
        super().__init__()
        self.invalidated = False
        self.selected = False
        self.selection_color = QColor(255, 0, 0, 40)
        self.index = index
        self.renderer = renderer
        self.ratio = ratio
        self.setTransform(QTransform(ratio, 0, 0, 0, ratio, 0, 0, 0, 1))
        self.view = view
        self.image = None
        self.original_size = size
        self.setRect(QRectF(0, 0, size.width(), size.height()))

        self.request_image_timer = QTimer()
        self.request_image_timer.setSingleShot(True)
        self.request_image_timer.timeout.connect(self.get_image_from_renderer)
        self.setAcceptTouchEvents(True)

    def invalidate(self, now=False):
        # Page may have changed size or orientation
        self.original_size = self.renderer.get_page_size(self.index)
        self.setRect(QRectF(0, 0, self.original_size.width(), self.original_size.height()))

        # Necessary to force the page to be updated immediately
        self.image = None if now else self.image

        self.invalidated = True
        self.update()

    def get_ratio(self):
        return self.ratio

    def get_original_size(self):
        return self.original_size

    def get_zoomed_size(self):
        return self.get_original_size() * self.ratio

    def get_index(self):
        return self.index

    def get_view(self):
        return self.view

    def update_ratio(self, ratio):
        self.ratio = ratio
        self.setTransform(QTransform(ratio, 0, 0, 0, ratio, 0, 0, 0, 1))
        # self.image = None
        self.invalidated = True
        self.update()

    def request_image(self, ratio, now=False):
        self.request_image_timer.stop()
        self.request_image_timer.start(200 if not now else 5)

    def get_image_from_renderer(self):
        self.image = self.renderer.render_page(self.index, self.ratio)
        self.invalidated = False
        self.update()

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        super().paint(painter, option, widget)
        # print("painting", self.index, self.image)
        if self.image is None or self.invalidated:
            self.request_image(self.ratio, self.image is None)

        if self.image is not None:
            painter.drawImage(QRectF(1, 1, self.rect().width() - 1, self.rect().height() - 1), self.image.toImage())

        if self.selected:
            painter.setBrush(QBrush(self.selection_color))
            painter.drawRect(QRect(1, 1, int(self.rect().width() - 1), int(self.rect().height() - 1)))

    def set_selected(self, value):
        self.selected = value
        self.update()

    def __repr__(self):
        return f"SwikPage({self.index}, {self.original_size}, {self.ratio})"

    def set_index(self, number):
        self.index = number

    def left(self):
        return self.sceneBoundingRect().left()

    def right(self):
        return self.sceneBoundingRect().right()

    def top(self):
        return self.sceneBoundingRect().top()

    def bottom(self):
        return self.sceneBoundingRect().bottom()

    def mid(self):
        return self.sceneBoundingRect().center()

    def height(self):
        return self.sceneBoundingRect().height()

    def width(self):
        return self.sceneBoundingRect().width()