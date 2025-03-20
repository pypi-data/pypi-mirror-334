from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPalette, QKeySequence
from PyQt5.QtWidgets import QGraphicsView, QScrollBar, QShortcut

from swikv4.pages.swik_miniature_page import SwikMiniaturePage
from swikv4.views.swik_view import SwikView


class MyScrollBar(QScrollBar):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def paintEvent(self, a0):
        super().paintEvent(a0)
        painter = QPainter(self)

        if self.maximum() != 0:
            return
        # use brush same color as the window (gray)
        # color = self.parent().palette().parent().color(self.backgroundRole())
        painter.setBrush(self.color)
        painter.setPen(self.color)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.end()


class SwikMiniatureView(SwikView):

    def __init__(self, scene, renderer):
        super().__init__(scene, renderer)
        self.highlighted_page = 0
        self.setMinimumWidth(180)
        self.setMaximumWidth(300)
        self.layout_manager.fit_width_border = 20
        self.layout_manager.lower_border = 60
        self.layout_manager.sep = 30
        self.layout_manager.adjust_scene_to_viewport = False
        self.layout_manager.set_mode(self.layout_manager.MODE_FIT_WIDTH)

        palette = self.palette()
        color = palette.color(QPalette.Window)

        self.setVerticalScrollBar(MyScrollBar(color))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        sc = QShortcut(QKeySequence(Qt.Key_Down), self)
        sc.activated.connect(self.page_down)
        sc = QShortcut(QKeySequence(Qt.Key_Up), self)
        sc.activated.connect(self.page_up)

    def page_up(self):
        self.move_to_page(self.current_page_number - 1)
        self.page_clicked.emit(self.current_page_number)

    def page_down(self):
        self.move_to_page(self.current_page_number + 1)
        self.page_clicked.emit(self.current_page_number)

    def create_page(self, index, size):
        page = SwikMiniaturePage(index, size, self.layout_manager.get_ratio(), self, self.renderer)
        return page

    def _set_page_number(self, page_number):
        super()._set_page_number(page_number)
        self.pages[self.highlighted_page].set_selected(False)
        self.pages[page_number].set_selected(True)
        self.highlighted_page = page_number

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        # In miniature view we don't want
        # to update the page when scrolling
        QGraphicsView.scrollContentsBy(self, dx, dy)

    def view_document_changed(self):
        # The pages must be created as the master view
        # creates its own, so the miniature view is filled at the same time
        # To this en we do nothing here and react to master_view_page_created
        self.highlighted_page = 0

    def master_view_page_created(self, index, last):
        if index == 0:
            # This is like the "document changed" event
            self.pages.clear()
            self.scene().clear()
            self.layout_manager.clear()
            self.highlighted_page = 0

            for i in range(self.renderer.get_document_length()):
                size = self.renderer.get_page_size(i)
                self.layout_manager.update_max_size(size)

        # Here we create the page already created by the master view
        size = self.renderer.get_page_size(index)
        page = self.create_page(index, size)
        self.scene().addItem(page)
        self.layout_manager.set_page_position_and_ratio(page)
        self.pages.append(page)
        self.layout_manager.adjust_scene_rect()

        if last:
            # Here we finish the document creation
            # self.layout_manager.adjust_scene_rect()
            self._set_page_number(0)

        # TODO:Introduced to make the miniature view more beautiful during loading

    def ensure_page_visible(self, page_number):
        super().ensure_page_visible(page_number)
        self.pages[self.highlighted_page].set_selected(False)
        self.pages[page_number].set_selected(True)
        self.highlighted_page = page_number

    def page_updated(self, index, need_layout_update=False):
        super().page_updated(index, need_layout_update)
