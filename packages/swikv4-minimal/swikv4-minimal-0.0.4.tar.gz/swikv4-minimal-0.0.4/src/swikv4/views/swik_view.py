from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QApplication

from swikv4.pages.swik_page import SwikPage
from swikv4.views.swik_layout_manager import SwikLayoutManager


class SwikView(QGraphicsView):
    # Page Number, total pages
    page_number_changed = pyqtSignal(int, int)

    document_ready = pyqtSignal()

    # Page Number
    page_clicked = pyqtSignal(int)

    # Page Number, is last
    page_created = pyqtSignal(int, bool)

    def __init__(self, scene, renderer):
        super().__init__(scene)
        self.current_page_number = 0
        self.pages = []
        self.setAlignment(Qt.AlignTop)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setResizeAnchor(self.AnchorUnderMouse)
        # self.setDragMode(self.ScrollHandDrag)
        # self.setRenderHint(self.Antialiasing)
        # self.setRenderHint(self.TextAntialiasing)
        # self.setRenderHint(self.SmoothPixmapTransform)
        # self.setRenderHint(self.HighQualityAntialiasing)
        # self.setRenderHint(self.NonCosmeticDefaultPen)
        self.renderer = renderer
        self.renderer.document_changed.connect(self.view_document_changed)
        self.renderer.page_updated.connect(self.page_updated)
        self.layout_manager = SwikLayoutManager(self, renderer)

    def move_to_page(self, page_number):
        if page_number < 0 or page_number >= len(self.pages):
            page_number = self.current_page_number
        else:
            self.layout_manager.move_to_page(page_number)
        self._set_page_number(page_number)

    def ensure_page_visible(self, page_number):
        # This "if" is necessary because the signal that generates
        # it is received by miniature too and at the beginning is not ready
        if page_number < len(self.pages):
            self.ensureVisible(self.pages[page_number])

    def get_current_page_number(self):
        return self.current_page_number

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        super().scrollContentsBy(dx, dy)
        for elem in self.get_visible_items():
            if isinstance(elem, SwikPage):
                if self.current_page_number != elem.get_index():
                    self._set_page_number(elem.get_index())
        # print("SB", self.verticalScrollBar().maximum(), self.verticalScrollBar().minimum(), self.verticalScrollBar().value(),
        #      self.scene().sceneRect().height(), self.verticalScrollBar().value() + self.viewport().height() - self.verticalScrollBar().minimum())

    def wheelEvent(self, event) -> None:
        if QApplication.keyboardModifiers() != Qt.ControlModifier:
            super().wheelEvent(event)
        else:
            anchor = event.pos()
            if event.angleDelta().y() > 0:
                self.zoom(self.get_ratio() * 1.1, anchor)
            else:
                self.zoom(self.get_ratio() * 0.9, anchor)
            # self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().maximum() / 2))

    def get_layout_manager(self):
        return self.layout_manager

    def view_document_changed(self):
        self.pages.clear()
        self.scene().clear()
        self.layout_manager.clear()

        for i in range(self.renderer.get_document_length()):
            size = self.renderer.get_page_size(i)
            self.layout_manager.update_max_size(size)

        for i in range(self.renderer.get_document_length()):
            size = self.renderer.get_page_size(i)
            page = self.create_page(i, size)
            self.pages.append(page)
            self.scene().addItem(page)
            self.layout_manager.set_page_position_and_ratio(page)
            self.page_created.emit(i, i == self.renderer.get_document_length() - 1)  # noqa
            QApplication.processEvents()

            # TODO: Introduced to make the the view more beautiful
            # during loading. Does not seem to affect speed
            self.layout_manager.bound_layout()

        self.layout_manager.bound_layout()
        self._set_page_number(0)
        QTimer.singleShot(0, self.document_ready.emit)

    def zoom(self, value, anchor=None):
        on_page, v_percent, page = None, None, None

        if anchor is not None:
            page: SwikPage = self.get_item_at_position(anchor, SwikPage)

        if page is not None:
            on_scene = self.mapToScene(anchor)
            on_page = page.mapFromScene(on_scene)
        elif self.verticalScrollBar().maximum() > 0:
            v_percent = self.verticalScrollBar().value() / self.verticalScrollBar().maximum()

        # Here we actually set the ratio, before and
        # after we calculate and reestablish the scrollbars
        self.layout_manager.set_ratio(value, anchor)

        if page is not None:
            on_scene = page.mapToScene(on_page)
            on_view = self.mapFromScene(on_scene)
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + int(on_view.y() - anchor.y()))
        elif self.verticalScrollBar().maximum() > 0:
            self.verticalScrollBar().setValue(int(v_percent * self.verticalScrollBar().maximum()))

        self.horizontalScrollBar().setValue(
            int(self.horizontalScrollBar().maximum() / 2 + self.horizontalScrollBar().minimum() / 2))

    def set_visualization_mode(self, mode, ratio=None):

        if self.verticalScrollBar().maximum() > 0:
            v_percent = self.verticalScrollBar().value() / self.verticalScrollBar().maximum()

        self.layout_manager.set_mode(mode, ratio)

        if self.verticalScrollBar().maximum() > 0:
            self.verticalScrollBar().setValue(int(v_percent * self.verticalScrollBar().maximum()))

    def get_ratio(self):
        return self.layout_manager.get_ratio()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.layout_manager.view_resized()

    def get_pages(self):
        return self.pages

    def get_page(self, index):
        if index is None or index >= len(self.pages) or index < 0:
            return None
        return self.pages[index]

    def get_visible_items(self):
        viewport_rect = self.viewport().rect()
        scene_rect = self.mapToScene(viewport_rect).boundingRect()
        return self.scene().items(scene_rect) if self.scene() else []

    def get_current_page(self):
        return self.pages[self.current_page_number]

    def get_items_at_position(self, pos, kind=None, strict=False):
        items = self.items(pos)
        if kind is None:
            return items
        if strict is False:
            return [item for item in items if isinstance(item, kind)]
        return [item for item in items if type(item) == kind]

    def get_item_at_position(self, pos, kind=None, index=0, strict=False):
        items = self.get_items_at_position(pos, kind, strict)
        if len(items) > index:
            return items[index]
        return None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # get page under the click
        items = self.get_items_at_position(event.pos(), SwikPage)
        if len(items) > 0:
            self.page_clicked.emit(items[0].get_index())  # type: ignore
            self._set_page_number(items[0].get_index())  # noqa

    def _set_page_number(self, page_number):
        self.current_page_number = page_number
        self.page_number_changed.emit(self.current_page_number, len(self.pages))  # noqa

    def create_page(self, index, size):
        return SwikPage(index, size, self.layout_manager.get_ratio(), self, self.renderer)

    def page_updated(self, index, need_layout_update=False):
        # True is necessary to force the page to be updated
        # immediately otherwise the pixmap would look weird
        self.pages[index].invalidate(True)
        if need_layout_update:
            self.layout_manager.update()
