
from PyQt6.QtWidgets import(
        QApplication,
        QMainWindow,
        QTextEdit,
        QFileDialog,
        QMessageBox,
        QWidget,
        QVBoxLayout,
        QPushButton,
        
)

class MainMenu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("background-color: black; font-size: 20px;")

        # place the menu on window using a vertical box layout
        layout = QVBoxLayout()
        
        button = QPushButton('Click me')
        button.setObjectName("fontButton")
        button.setCheckable(True)
        # Apply the stylesheet
        button.setStyleSheet("""
            QPushButton#fontButton {
                font-size: 20px;
            }
            QPushButton#fontButton:hover {
                background-color: lightsteelblue;
            }               
        """)
        layout.addWidget(button)
        
        self.setLayout(layout)