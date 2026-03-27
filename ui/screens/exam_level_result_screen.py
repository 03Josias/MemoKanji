from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,QHBoxLayout, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from ui.screens.study_screen import StudyScreen
from ui.sounds.sound_manager import SoundManager

class ExamLevelResultScreen(QWidget):

    def __init__(self, main_window, nivel, passed, correct, stars):
        super().__init__()

        self.main_window = main_window
        self.nivel = nivel

        self.passed = passed
        self.correct = correct
        self.stars = stars

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
        if self.passed:
            title_text = "COMPLETADO"
            color = "#02b072"
        else:
            title_text = "DESAPROBADO"
            color = "#a14549"

        title = QLabel(title_text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {color};")
        layout.addWidget(title)

        # Puntaje
        score = QLabel(f"Aciertos: {self.correct} / 50")
        score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score.setFont(QFont("Arial", 22))
        score.setStyleSheet("color: #d4d2d2;")
        layout.addWidget(score)

        # # Estrellas
        # if self.passed:
        #     stars_label = QLabel("⭐" * self.stars)
        #     stars_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #     stars_label.setFont(QFont("Arial", 30))
        #     layout.addWidget(stars_label)
        #     print(self.stars)
        if self.passed:
            stars_layout = QHBoxLayout()
            stars_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stars_layout.setSpacing(15)

            self.star_widgets = []

            for i in range(self.stars):
                star = QLabel("⭐")
                star.setFont(QFont("Arial", 40))
                star.setAlignment(Qt.AlignmentFlag.AlignCenter)
                opacity = QGraphicsOpacityEffect()
                opacity.setOpacity(0)  # invisible pero ocupa espacio

                star.setGraphicsEffect(opacity)
                star.opacity_effect = opacity
                stars_layout.addWidget(star)
                self.star_widgets.append(star)


            layout.addLayout(stars_layout)
            from ui.animations.star_animation import animate_stars
            QTimer.singleShot(300, lambda: animate_stars(self.star_widgets))
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
        from ui.screens.level_exam_screen import LevelExamScreen
        screen = LevelExamScreen(
            self.main_window,
            self.nivel
        )
        self.main_window.change_screen(screen)
    
    def go_back(self):
        study_screen=StudyScreen(self.main_window)
        self.main_window.change_screen(study_screen)

  