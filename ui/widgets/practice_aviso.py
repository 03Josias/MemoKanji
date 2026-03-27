
from ctypes import alignment
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.screens.home_screen import HomeScreen
from ui.sounds.sound_manager import SoundManager

class PracticeAviso(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        board = QWidget()
        board.setObjectName("board")
        board.setMinimumSize(750, 450)
        board.setStyleSheet("""
            QWidget#board {
                background-color: #2E6F57;
                border: 10px solid #8B5A2B;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Título
        title_text = "Completa el primero modulo para practicar"
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #d4d2d2;")

        layout.addWidget(title)

        # Botones
        exit_btn = QPushButton("Volver")
        exit_btn.setFixedSize(125, 60)
        exit_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        exit_btn.setStyleSheet("""
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
        exit_btn.clicked.connect(SoundManager.play_click)
        exit_btn.clicked.connect(self.go_back) 

        layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        board.setLayout(layout)

        main_layout.addWidget(board, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def go_back(self):
        self.main_window.navigate_to(self.main_window.home_screen)

