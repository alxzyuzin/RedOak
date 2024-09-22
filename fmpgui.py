import sys
from PyQt6.QtCore import Qt,QPoint
from PyQt6.QtGui import QPalette, QColor, QIcon, QRegion, QPainterPath
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)

from SMAModules.WindowHeader import WindowHeader 
from SMAModules.WorkArea import WorkArea

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setGeometry(100, 100, 500, 300)
        # Remove the title bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.window_content = QWidget()
       
        self.work_area = WorkArea(self)
        self.title_bar = WindowHeader()
        layout = QVBoxLayout(self)
        layout.addWidget(self.title_bar)
        layout.addWidget(self.work_area)
        layout.setStretchFactor(self.title_bar, 0)
        layout.setStretchFactor(self.work_area, 2)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.window_content.setLayout(layout)

        self.setCentralWidget(self.window_content)
  
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet('font-size:18px')
                  
    def resizeEvent(self, event):
        # Update the mask when the window is resized
        # Create a rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 4, 4)
        # Set the mask to the rounded rectangle
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
    
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    # create the main window and display it
    window = MainWindow()
     # show the window
    window.show()
    # start the event loop
    sys.exit(app.exec())