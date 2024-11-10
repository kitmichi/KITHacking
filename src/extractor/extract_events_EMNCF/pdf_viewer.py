import random
import sys
import tempfile
from pathlib import Path

import fitz  # PyMuPDF
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QRadioButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from extractor.extract_events_EMNCF.create_events import write_files


class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.page_number = 4
        self.temp_dir_tempfile = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.temp_dir = Path(self.temp_dir_tempfile.name)
        self.rects = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Viewer")
        width, height = self.get_dimensions()
        self.setGeometry(0, 0, width, height)

        # Create a central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)
        self.root_pixmap = self.render_page(self.page_number)
        self.label.setPixmap(self.root_pixmap)
        self.layout.addWidget(self.label)

        # Add radio buttons
        self.radios = [
            QRadioButton("Lecture", self),
            QRadioButton("Lecture negative", self),
            QRadioButton("Exercise", self),
        ]
        for radio in self.radios:
            self.layout.addWidget(radio)
        self.radios[0].setChecked(True)  # Set radio1 as checked by default

        # Enable mouse tracking
        self.setMouseTracking(True)
        self.central_widget.setMouseTracking(True)
        self.label.setMouseTracking(True)

        self.start_pos = None
        self.end_pos = None

        # Add a status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.show()

    def get_dimensions(self):
        page = self.doc[0]
        pix = page.get_pixmap()
        return pix.width, pix.height

    def render_page(self, page_number):
        page = self.doc.load_page(page_number)
        pix = page.get_pixmap()
        img = QPixmap.fromImage(
            QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        )
        return img

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = self.label.mapFromGlobal(event.globalPos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_pos:
            self.end_pos = self.label.mapFromGlobal(event.globalPos())
            self.highlight_area()
        self.start_pos = None
        self.end_pos = None

    def mouseMoveEvent(self, event):
        # Convert the global mouse position to the label's coordinate system
        label_pos = self.label.mapFromGlobal(event.globalPos())
        self.end_pos = label_pos
        # Update the status bar with the current mouse position relative to the label
        self.statusBar.showMessage(f"Mouse position relative to label: {label_pos}")
        self.highlight_area_gui()

    def highlight_area_gui(self):
        if not (self.start_pos and self.end_pos):
            return
        self.label.setPixmap(self.root_pixmap)

        rect = QRect(self.start_pos, self.end_pos)
        for radio in self.radios:
            if radio.isChecked():
                selected_radio = radio
        key = selected_radio.text()
        if key not in self.rects:
            self.rects[key] = {
                "rect": rect,
                "color": QColor(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                ),
            }
        else:
            self.rects[key]["rect"] = rect

        painter = QPainter(self.label.pixmap())
        for key, rect in self.rects.items():
            pen = QPen(
                rect["color"],
                3,
                Qt.SolidLine,
            )
            painter.setPen(pen)
            painter.drawRect(rect["rect"])
        painter.end()
        self.label.update()

    def highlight_area(self):
        if not (self.start_pos and self.end_pos):
            return
        self.highlight_area_gui()
        rect = QRect(self.start_pos, self.end_pos)

        # Convert QRect to fitz.Rect and add highlight annotation
        page = self.doc.load_page(self.page_number)
        fitz_rect = fitz.Rect(rect.left(), rect.top(), rect.right(), rect.bottom())
        print(fitz_rect)
        page.add_highlight_annot(fitz_rect)

        # Extract and print text from the selected rectangle
        text = page.get_textbox(fitz_rect).strip()
        print(f"Extracted text:\n{text}")
        for radio in self.radios:
            if radio.isChecked():
                file = radio.text()
        with open(self.temp_dir / f"{file}.txt", "w") as f:
            f.write(text)

        self.doc.save(
            self.temp_dir / f"{self.pdf_path.stem}_highlighted{self.pdf_path.suffix}"
        )

        write_files(self.temp_dir)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer(
        Path(__file__).parent / "EMNCF_00_Organization_Introduction_WS2024.pdf"
    )
    sys.exit(app.exec_())
