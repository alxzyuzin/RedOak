
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
class WindowHeader(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent_widget = parent
        
        p = self.palette()
        p.setColor(QPalette.ColorRole.Window, QColor('#717171'))
        self.setPalette(p)
        self.setAutoFillBackground(True)
        
        self.title_label = QLabel("Custom Title Bar", self)
        self.title_label.setObjectName('tlbl')
        self.title_label.setStyleSheet("QLabel#tlbl { background-color: #717171; color: #FFFFFF; font-size: 18px; margin-left: 10px;  }")
              
        self.collapse_button = QPushButton(self)
        self.collapse_button.setIcon(QIcon("assets\\minus.svg"))
        self.collapse_button.setIconSize(QSize(20, 20)) 
        self.collapse_button.clicked.connect(self.collapseParent)
        self.collapse_button.setObjectName("collapse_btn")
        self.collapse_button.setStyleSheet("QPushButton#collapse_btn{ background-color: #717171;} QPushButton#collapse_btn:hover { background-color: #A1A1A1;}")     
        
        self.expand_button = QPushButton(self)
        self.expand_button.setIcon(QIcon("assets\\square.svg"))
        self.expand_button.setIconSize(QSize(20, 20)) 
        self.expand_button.clicked.connect(self.expandParent)
        self.expand_button.setObjectName("expand_btn")
        self.expand_button.setStyleSheet("QPushButton#expand_btn{ background-color: #717171;} QPushButton#expand_btn:hover { background-color: #A1A1A1;}")     
        
        self.close_button = QPushButton(self)
        self.close_button.setIcon(QIcon("assets\\close.svg"))
        self.close_button.setIconSize(QSize(20, 20)) 
        self.close_button.setObjectName("close_btn")
        self.close_button.setStyleSheet("""
                        QPushButton#close_btn {
                            background-color: #717171; 
                            } 
                        QPushButton#close_btn:hover {
                            background-color: #FF0000;
                            } 
                        QPushButton#close_btn:pressed {
                            background-color: #CC0000;
                            }                 
                        """)
        
        self.close_button.clicked.connect(self.closeParent)
                 
        # Layout for the title bar
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.collapse_button)
        layout.addWidget(self.expand_button)
        layout.addWidget(self.close_button)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(layout)
          
    def closeParent(self):
        if self.parent_widget != None:
            self.parent_widget.close()

    def collapseParent(self):
        pass

    def expandParent(self):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.startPos:
            delta = QPoint(event.globalPosition().toPoint() - self.startPos)
            self.window().move(self.window().pos() + delta)
            self.startPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.startPos = None

        