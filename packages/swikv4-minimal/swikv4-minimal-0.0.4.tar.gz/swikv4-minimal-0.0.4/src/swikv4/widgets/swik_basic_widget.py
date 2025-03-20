import resource  # noqa

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QShortcut, QSplitter

from swikv4.renderers.swik_renderer import SwikRenderer
from swikv4.scenes.swik_scene import SwikScene
from swikv4.toolbars.swik_page_navigation_toolbar import SwikPageNavigationToolbar
from swikv4.toolbars.swik_zoom_toolbar import SwikZoomToolbar
from swikv4.views.swik_miniature_view import SwikMiniatureView
from swikv4.views.swik_view import SwikView


class SwikBasicWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())

        self.renderer = SwikRenderer()
        self.scene = SwikScene()
        self.view = SwikView(self.scene, self.renderer)

        self.miniature_scene = SwikScene()
        self.miniature_view = SwikMiniatureView(self.miniature_scene, self.renderer)
        self.miniature_view.page_clicked.connect(self.view.move_to_page)
        self.view.page_created.connect(self.miniature_view.master_view_page_created)

        self.zoom_toolbar = SwikZoomToolbar(self.view)
        self.zoom_toolbar.toolbar().addSeparator()
        self.page_toolbar = SwikPageNavigationToolbar(self.view, self.renderer, self.zoom_toolbar.toolbar())
        self.zoom_toolbar.toolbar().addSeparator()

        self.layout().addWidget(self.zoom_toolbar.toolbar())

        self.splitter = QSplitter()
        self.splitter.addWidget(self.miniature_view)
        self.splitter.addWidget(self.view)
        self.layout().addWidget(self.splitter)

        # add ctrl++ and ctrl+- to zoom in and out

        sc = QShortcut(QKeySequence('Ctrl++'), self)
        sc.activated.connect(lambda: self.view.zoom(self.view.get_ratio() * 1.1))

        sc = QShortcut(QKeySequence('Ctrl+-'), self)
        sc.activated.connect(lambda: self.view.zoom(self.view.get_ratio() * 0.9))

        sc = QShortcut(QKeySequence('Ctrl+M'), self)
        sc.activated.connect(self.change_mode)

        self.view.page_number_changed.connect(self.miniature_view.ensure_page_visible)

        self.show()

    def change_mode(self):
        self.view.layout_manager.loop_mode()

    def closing(self):
        pass

    def get_filename(self):
        return self.renderer.get_filename()

    def get_mode(self):
        return self.view.layout_manager.get_mode()

    def get_ratio(self):
        return self.view.get_ratio()

    def get_page_number(self):
        return self.view.get_current_page_number()

    def open(self, filename, **kwargs):
        self.view.layout_manager.set_mode(kwargs.get("mode", self.view.layout_manager.MODE_GRID),
                                          kwargs.get("ratio", 1.0))
        self.renderer.open_document(filename)
        self.view.move_to_page(kwargs.get("index", 0))
