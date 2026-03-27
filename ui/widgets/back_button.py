
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont
from ui.sounds.sound_manager import SoundManager


class BackButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__("←", parent)
        self.clicked.connect(SoundManager.play_click)

        self.setFixedSize(40, 40)
        self.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        self.setStyleSheet("""
            QPushButton {
                background-color: #3A7761;
                border-radius: 18px;
                color: #d4d2d2;
                }
            QPushButton:hover {
                background-color: #316351;
                }
            QPushButton:pressed {
                background-color: #285243;
                }
            """)