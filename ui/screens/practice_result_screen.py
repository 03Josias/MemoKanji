from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.screens.practice_screen import PracticeScreen
from ui.sounds.sound_manager import SoundManager

class PracticeResultScreen(QWidget):

    def __init__(self, main_window, current_streak,max_streak,total_seen,all_kanji,no_more):
        super().__init__()

        self.main_window = main_window
        self.current_streak = current_streak
        self.max_streak = max_streak
        self.total_seen = total_seen
        self.all_kanji = all_kanji
        self.no_more = no_more
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        board = QWidget()
        board.setObjectName("board")
        board.setMinimumSize(1000, 650)

        board.setStyleSheet("""
            QWidget#board {
                background-color: #2E6F57;
                border: 10px solid #8B5A2B;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        # Título
        if self.no_more:
            if self.total_seen == self.all_kanji:
                title_text = "¡Felicidades!\nHas practicado todos los kanji disponibles."
                color = "#02b072"
            else:
                title_text = "No hay más kanji disponibles.\nContinúa estudiando para desbloquear más."
                color = "#02b072"
        else:
            title_text = "Fin de la práctica"
            color = "#a14549"

        title = QLabel(title_text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 30, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {color};")
        layout.addWidget(title)

        # Puntaje
        score = QLabel(f"Racha: {self.current_streak}")
        score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score.setFont(QFont("Arial", 22))
        score.setStyleSheet("color: #d4d2d2;")
        layout.addWidget(score)

        # Record
        record_label= QLabel(f"Record: {self.max_streak}")
        record_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        record_label.setFont(QFont("Arial", 22))
        record_label.setStyleSheet("color: #d4d2d2;")
        layout.addWidget(record_label)

        # Botones
        retry_btn = QPushButton("Reintentar")
        retry_btn.clicked.connect(self.retry_exam)

        exit_btn = QPushButton("Salir")
        exit_btn.clicked.connect(self.go_back)


        for btn in [retry_btn, exit_btn]:
            btn.setFixedSize(250, 60)
            btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                background-color: #3A7761;
                border-radius: 18px;
                }
                QPushButton:hover {
                    background-color: #316351;
                }
                QPushButton:pressed {
                    background-color: #285243;
                }
        """)
            btn.clicked.connect(SoundManager.play_click)

            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            from ui.animations.hover_animation import apply_hover_scale
            apply_hover_scale(btn)
        board.setLayout(layout)
        main_layout.addWidget(board)
        self.setLayout(main_layout)

    def retry_exam(self):
        screen = PracticeScreen(self.main_window)
        self.main_window.change_screen(screen)

    def go_back(self):
        self.main_window.navigate_to(self.main_window.home_screen)

