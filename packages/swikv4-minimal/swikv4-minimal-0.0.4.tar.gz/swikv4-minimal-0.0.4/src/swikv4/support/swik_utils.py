import fitz
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QImage, QColor
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QGroupBox, QLabel, QSizePolicy
from pymupdf import Point


class Framed(QGroupBox):
    def __init__(self, title):
        super().__init__()
        self.setStyleSheet(
            "QGroupBox {border: 1px solid silver; border-radius: 2px; margin-top: 10px;}"
            "QGroupBox::title { subcontrol-origin: margin;    left: 7px;  padding: 0px 5px 0px 5px;}")

        self.setTitle(title if title else "")
        self.setLayout(QVBoxLayout())


class VFramed(Framed):
    def __init__(self, title, *args, **kwargs):
        super().__init__(title)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(VHelper(*args, **kwargs))


class HFramed(Framed):
    def __init__(self, title, *args, **kwargs):
        super().__init__(title)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(HHelper(*args, **kwargs))


class Helper(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs.get('orientation', Qt.Horizontal) == Qt.Horizontal:
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        for widget in args:
            if type(widget) == str:
                widget = QLabel(widget)
            self.layout().addWidget(widget, 0)
        self.layout().setSpacing(kwargs.get('spacing', 2))

        if kwargs.get('minwidth', None):
            self.setMinimumWidth(kwargs.get('minwidth'))
        if kwargs.get('minheight', None):
            self.setMinimumHeight(kwargs.get('minheight'))
        if kwargs.get('maxwidth', None):
            self.setMaximumWidth(kwargs.get('maxwidth'))
        if kwargs.get('maxheight', None):
            self.setMaximumHeight(kwargs.get('maxheight'))

        self.layout().setAlignment(kwargs.get("alignment", Qt.AlignTop))


class VHelper(Helper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, orientation=Qt.Vertical, **kwargs)


class HHelper(Helper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, orientation=Qt.Horizontal, **kwargs)


def rect_to_pdf_coordinates(filename, index, rect):
    # The signing is not done using PyMuPDF, so we need to compute
    # the square in the pyhanko page (which to make everything
    # more complicated uses upside-down coordinates (notice dy))
    # We need to get some info from the file that is about to be signed
    # that can be different from the one we are seeing (e.g. flatten + sign)

    # Open the doc to sign
    doc_to_sign = fitz.open(filename)

    # The projection is necessary to take into account orientation
    # rot = self.renderer.get_rotation(page.index)
    rot = doc_to_sign[index].rotation

    # Get page size
    # w, h = self.renderer.get_page_size(page.index)
    w, h = doc_to_sign[index].rect[2], doc_to_sign[index].rect[3]

    # Get derotation matrix
    derot_matrix = doc_to_sign[index].derotation_matrix

    # Close the file, it is not needed anymore
    doc_to_sign.close()

    # Take into account that pyhanko uses upside-down coordinates
    dy = w if rot == 90 or rot == 270 else h

    # Rotate according to the orientation and create thw box
    # r1 = self.renderer.project(fitz.Point(rect.x(), rect.y()), page.index)
    r1 = Point(rect.x(), rect.y()) * derot_matrix
    box = (r1.x,
           dy - r1.y,
           r1.x + rect.width(),
           dy - (r1.y + rect.height()))
    return box


def move_items(lst, items, after_value, after=True):
    for item in items:
        lst.remove(item)

    if after:
        items.reverse()

    for item in items:
        index = lst.index(after_value)
        lst.insert(index + after, item)

    return lst


def framed(widget, title=None):
    frame = QGroupBox()
    frame.setStyleSheet(
        "QGroupBox {border: 1px solid silver; border-radius: 2px; margin-top: 10px;}"
        "QGroupBox::title { subcontrol-origin: margin;    left: 7px;  padding: 0px 5px 0px 5px;}")

    frame.setTitle(title if title else "")
    frame.setLayout(QVBoxLayout())
    # frame.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    if isinstance(widget, QWidget):
        frame.layout().addWidget(widget)
    else:
        frame.layout().addLayout(widget)

    return frame


def adjust_crop(image: QImage, ratio=1.0, level=255) -> QRectF:
    # Initialize variables for the dimensions of the smallest rectangle
    # that contains non-white pixels
    left = image.width()
    top = image.height()
    right = 0
    bottom = 0

    # Iterate over all pixels in the image
    for x in range(image.width()):
        for y in range(image.height()):
            # Get the color of the current pixel
            color = QColor(image.pixel(x, y))
            r, g, b = color.red(), color.green(), color.blue()
            # If the color is not white, update the dimensions of the
            # smallest rectangle that contains non-white pixels
            if r < level or g < level or b < level:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    # Return the smallest rectangle that contains non-white pixels
    return QRectF(left / ratio, top / ratio, (right - left) / ratio + 2, (bottom - top) / ratio + 2)
