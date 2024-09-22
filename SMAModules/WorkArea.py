from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtWidgets import(
        QApplication,
        QMainWindow,
        QTextEdit,
        QFileDialog,
        QMessageBox,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QPushButton,
        QLabel
        
)

# Custom title bar
class WorkArea(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent_widget = parent

        p = self.palette()
        p.setColor(QPalette.ColorRole.Window, QColor('#8E8E8E'))
        self.setPalette(p)
        self.setAutoFillBackground(True)