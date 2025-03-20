from PyQt5.QtCore import pyqtSignal, QObject

from swikv4.pages.swik_page import SwikPage


class SwikLayoutManager(QObject):
    MODE_FIT_WIDTH = 0
    MODE_VERTICAL_SCROLL = 1
    MODE_GRID = 2

    modes = ["Fit Width", "Vertical Scroll", "Grid"]

    layout_mode_changed = pyqtSignal(int, float)

    def __init__(self, view, renderer):
        super().__init__()
        self.rows = []
        self.lower_border = 30
        self.upper_border = 15
        self.adjust_to_viewport = True
        self.fallback_layout_mode = SwikLayoutManager.MODE_VERTICAL_SCROLL
        self.view = view
        self.layout_ratio = 1
        self.renderer = renderer
        self.pages_max_width = 0
        self.pages_max_height = 0
        self.current_y = 0
        self.page_grid_coordinates = {}

        # for grid mode
        self.current_x = 0
        # self.current_row = []

        self.sep = 20
        self.fit_width_border = 25
        self.layout_mode = SwikLayoutManager.MODE_FIT_WIDTH

    def update(self):
        self.compute_max_size()
        self.set_mode(self.layout_mode, self.layout_ratio)

    # Entry Point
    def set_page_position_and_ratio(self, page: SwikPage):
        if self.layout_mode == SwikLayoutManager.MODE_FIT_WIDTH:
            self._set_single_page_position_in_fit_width_mode(page)

        elif self.layout_mode == SwikLayoutManager.MODE_VERTICAL_SCROLL:
            self._set_single_page_position_in_vertical_scroll_mode(page)

        elif self.layout_mode == SwikLayoutManager.MODE_GRID:
            self._set_single_page_position_in_grid_mode(page)

    def loop_mode(self):
        mode = (self.layout_mode + 1) % 3
        self.set_mode(mode)
        return mode

    def set_mode(self, mode, ratio=None):
        self.layout_mode = mode
        if self.layout_mode == SwikLayoutManager.MODE_FIT_WIDTH:
            self.view_resized()
        else:
            self.layout_ratio = ratio if ratio is not None else self.layout_ratio
            self.clear()
            self._apply_ratio(self.layout_ratio)
        self.layout_mode_changed.emit(self.layout_mode, self.layout_ratio)

    def clear(self):
        self.pages_max_width = 0
        self.pages_max_height = 0
        self.current_y = 0
        self.page_grid_coordinates.clear()
        self.rows.clear()

    def update_max_size(self, size):
        self.pages_max_width = max(self.pages_max_width, size.width())
        self.pages_max_height = max(self.pages_max_height, size.height())

    def compute_max_size(self):
        for page in self.view.pages:
            self.update_max_size(page.get_original_size())

    def get_mode(self):
        return self.layout_mode

    def get_ratio(self):
        return self.layout_ratio

    def set_ratio(self, ratio, anchor=None):

        ratio = min(5, max(0.25, ratio))  # type: ignore

        if self.layout_mode == SwikLayoutManager.MODE_FIT_WIDTH:
            self.layout_mode = self.fallback_layout_mode
            ratio = self.view.get_current_page().ratio
        self._apply_ratio(ratio)

        self.view.viewport().update()

        self.layout_mode_changed.emit(self.layout_mode, ratio)  # type: ignore

    def _apply_ratio(self, ratio):
        self.clear()
        self.layout_ratio = ratio

        if self.layout_mode == SwikLayoutManager.MODE_VERTICAL_SCROLL:
            for page in self.view.pages:
                page.update_ratio(ratio)
                self._set_single_page_position_in_vertical_scroll_mode(page)
            self.adjust_scene_rect()


        elif self.layout_mode == SwikLayoutManager.MODE_GRID:
            for page in self.view.pages:
                page.update_ratio(ratio)
            self._set_pages_position_in_grid_mode()
            self.adjust_scene_rect()

    def view_resized(self):
        if self.layout_mode == SwikLayoutManager.MODE_FIT_WIDTH:
            self.clear()
            for page in self.view.pages:
                self._set_single_page_position_in_fit_width_mode(page)
            self.adjust_scene_rect()
        elif self.layout_mode == SwikLayoutManager.MODE_GRID:
            self._set_pages_position_in_grid_mode()
            self.adjust_scene_rect()

        # TODO: Not necessary? self.view.ensureVisible(self.view.get_current_page())

    def adjust_scene_rect(self):
        if self.layout_mode in [SwikLayoutManager.MODE_FIT_WIDTH, SwikLayoutManager.MODE_VERTICAL_SCROLL,
                                SwikLayoutManager.MODE_GRID]:
            br = self.view.scene().itemsBoundingRect()

            # TODO: Make scene bigger to fit the width of the viewport
            if self.adjust_to_viewport:
                diff_x = max(0, self.view.viewport().width() - br.width())
            else:
                diff_x = 0
            self.view.scene().setSceneRect(br.x() - diff_x / 2,
                                           br.y() - self.upper_border,
                                           br.width() + diff_x,
                                           br.height() + self.lower_border)
            # print("Adjusting scene rect", br)

    def move_to_page(self, index):
        page = self.view.get_page(index)
        if self.layout_mode in [SwikLayoutManager.MODE_FIT_WIDTH, SwikLayoutManager.MODE_VERTICAL_SCROLL,
                                SwikLayoutManager.MODE_GRID]:
            self.view.verticalScrollBar().setValue(int(page.y() - 16))

    def set_borders(self, upper, lower=None):
        if lower is None:
            lower = 2 * upper
        self.lower_border = lower
        self.upper_border = upper

    def bound_layout(self):
        self.adjust_scene_rect()

    ### Single Page Positioning

    def _set_single_page_position_in_fit_width_mode(self, page: SwikPage):
        view_size = self.view.viewport().size()
        page_size = page.get_original_size()
        ratio = (view_size.width() - self.fit_width_border * 2) / page_size.width()
        page.update_ratio(ratio)
        page.setPos(self.fit_width_border, self.current_y)
        self.current_y += page.get_zoomed_size().height() + self.sep
        self.page_grid_coordinates[page] = (page.index, 0, True)

    def _set_single_page_position_in_vertical_scroll_mode(self, page: SwikPage):
        page_size = page.get_zoomed_size()
        x = (self.pages_max_width - page_size.width()) / 2
        page.setPos(x, self.current_y)
        self.current_y += page_size.height() + self.sep
        self.page_grid_coordinates[page] = (page.index, 0, True)

    # def _set_single_page_position_in_grid_mode2(self, page):
    #     view_size = self.view.viewport().size()
    #     page_size = page.get_zoomed_size()
    #     current_width = 0
    #     current_max_height = 0
    #     print("setting page", page.index)
    #     for page_in_row in self.current_row:
    #         current_width += page_in_row.get_zoomed_size().width() + self.sep
    #         current_max_height = max(current_max_height, page_in_row.get_zoomed_size().height())
    #
    #     print("current width", current_width)
    #
    #     if current_width + page_size.width() + self.sep < view_size.width():
    #         page.setPos(current_width + self.sep, self.current_y)
    #         print("setting page", page.index, "at", current_width, self.current_y)
    #         self.current_row.append(page)
    #     else:
    #         self.current_y += current_max_height + self.sep
    #         self.current_row = [page]
    #         page.setPos(self.sep, self.current_y)
    #         print("setting page2", page.index, "at", current_width, self.current_y)

    def _set_single_page_position_in_grid_mode(self, page):
        self._set_pages_position_in_grid_mode()

    def _set_pages_position_in_grid_mode(self):
        max_row_width = 0
        rows, current_row = [], []
        for page in self.view.pages:

            view_size = self.view.viewport().size()
            page_size = page.get_zoomed_size()

            current_width, current_max_height = self.sep, 0

            for page_in_row in current_row:
                current_width += page_in_row.get_zoomed_size().width() + self.sep
                current_max_height = max(current_max_height, page_in_row.get_zoomed_size().height())

            if current_width + page_size.width() + self.sep < view_size.width() or len(current_row) == 0:
                current_row.append(page)
            else:
                rows.append((current_row, current_width, current_max_height))
                max_row_width = max(max_row_width, current_width)
                current_row = [page]

            if page == self.view.pages[-1]:
                current_width = sum([page_in_row.get_zoomed_size().width() + self.sep for page_in_row in current_row])
                rows.append((current_row, current_width + self.sep, current_max_height))

        current_y = 0
        for row_index, row in enumerate(rows):
            pages, width, height = row
            current_width = max_row_width / 2 - width / 2 + self.sep
            for col_index, page in enumerate(pages):
                page.setPos(current_width, height / 2 - page.get_zoomed_size().height() / 2 + current_y)
                current_width += page.get_zoomed_size().width() + self.sep
                self.page_grid_coordinates[page] = (row_index, col_index, col_index == len(pages) - 1)

            current_y += height + self.sep

    def get_page_grid_coordinates(self, page):
        return self.page_grid_coordinates[page]

    def aside(self, page1, page2):
        row1, col1, _ = self.get_page_grid_coordinates(page1)
        row2, col2, _ = self.get_page_grid_coordinates(page2)
        return row1 == row2 and abs(col1 - col2) == 1

    def above(self, page1, page2):
        row1, col1, _ = self.get_page_grid_coordinates(page1)
        row2, col2, _ = self.get_page_grid_coordinates(page2)
        return col1 == col2 and abs(row1 - row2) == 1

    def first_of_row(self, page):
        row, col, _ = self.get_page_grid_coordinates(page)
        return col == 0

    def last_of_row(self, page):
        row, col, last = self.get_page_grid_coordinates(page)
        return last
