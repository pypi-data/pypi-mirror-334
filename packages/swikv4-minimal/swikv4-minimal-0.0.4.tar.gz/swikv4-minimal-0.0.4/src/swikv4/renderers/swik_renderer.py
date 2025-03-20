import os
import tempfile

import pymupdf
from PyQt5.QtCore import QObject, pyqtSignal, QSizeF
from PyQt5.QtGui import QImage, QPixmap, QPainter


class SwikRenderer(QObject):
    document_changed = pyqtSignal(object)
    page_updated = pyqtSignal(int, bool)

    def __init__(self):
        super().__init__()
        self.document: pymupdf.Document = None  # noqa
        self.path = None

    def open_document(self, path, **kwargs):
        self.path = path
        self.document = pymupdf.open(path)
        self.document_changed.emit(kwargs)

    def get_filename(self):
        return self.path

    def render_page(self, index, ratio, annots=False):
        mat = pymupdf.Matrix(ratio, ratio)
        pix = self.document[index].get_pixmap(matrix=mat, alpha=False, annots=annots)
        page_image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

        # If there signature widgets, render them
        page = self.document[index]
        for field in page.widgets():  # type: pymupdf.Widget
            pix2 = self.document[index].get_pixmap(matrix=mat, alpha=False, annots=True, clip=field.rect)
            widget_image = QImage(pix2.samples, pix2.width, pix2.height, pix2.stride, QImage.Format_RGB888)
            painter = QPainter(page_image)
            painter.drawImage(int(field.rect.x0 * ratio), int(field.rect.y0 * ratio), widget_image)
            painter.end()

        return QPixmap.fromImage(page_image)

    def get_page_size(self, index):
        page: pymupdf.Page = self.document[index]
        return QSizeF(page.rect.width, page.rect.height)

    def get_document_length(self):
        return len(self.document)

    def close_document(self, save=False):
        if self.document.is_dirty and not save:
            return False

        if save:
            self.save_document()

        self.document.close()
        self.document = None
        return True

    def save_document(self, path=None, **kwargs):
        if path is None:
            path = self.path

        if path == self.path:
            if self.document.can_save_incrementally():
                self.document.saveIncr()
            else:
                temp_name = tempfile.mktemp()
                self.document.save(temp_name)
                self.document.close()
                os.rename(temp_name, path)
        else:
            self.path = path
            self.document.save(path)
            self.document.close()

    # def get_page_words(self, index):
    #     page: pymupdf.Page = self.document[index]
    #
    #     boxes = self.document[index].get_text("words", sort=True,
    #                                           flags=pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES)
    #
    #     words = list()
    #     for i, w in enumerate(boxes):
    #         x1, y1, x2, y2, text, block_no, line_no, word_no = w
    #         # Compute rectangle taking into account orientation
    #         fitz_rect = pymupdf.Rect(x1, y1, x2, y2) * self.document[index].rotation_matrix
    #         words.append(
    #             SwikWord(text, fitz_rect.x0, fitz_rect.y0, fitz_rect.width, fitz_rect.height, index, index * 10000 + i))
    #     return words
