import resource  # noqa
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from swikv4.widgets.swik_basic_widget import SwikBasicWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.basic_widget = SwikBasicWidget(self)
        self.setCentralWidget(self.basic_widget)
        menu = self.menuBar().addMenu("File")
        menu.addAction("Open", self.open_file)
        self.setMinimumHeight(600)
        self.show()

    def edit_config(self):
        if self.config.edit():
            self.config.save("swikv4.yaml")

    def open_file(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'Open file', '/home/danilo/Downloads', "PDF files (*.pdf)")
        if ok:
            try:
                self.basic_widget.renderer.open_document(filename)
            except Exception as e:
                # inform user about error
                QMessageBox.critical(self, "File corrupted", "File corrupted or not a PDF file")

    def closeEvent(self, a0):
        self.basic_widget.closing()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
