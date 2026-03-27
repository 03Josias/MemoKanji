from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.sounds.sound_manager import SoundManager


class ModuleOptionsScreen(QWidget):

    def __init__(self, main_window, nivel, modulo):
        super().__init__()

        self.main_window = main_window
        self.nivel = nivel
        self.modulo = modulo

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
        layout.setSpacing(40)

        # Título
        title = QLabel(f"MÓDULO {self.modulo}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: #d4d2d2;")

        layout.addWidget(title)

        # Botones
        study_btn = QPushButton("Estudiar")
        exam_btn = QPushButton("Hacer examen")
        back_btn = QPushButton("Volver")

        for btn in [study_btn, exam_btn, back_btn]:
            btn.setFixedSize(300, 70)
            btn.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                background-color: #3A7761;
                border-radius: 18px;
                color: #d4d2d2
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
        study_btn.clicked.connect(self.go_to_class)
        exam_btn.clicked.connect(self.go_to_exam)
        back_btn.clicked.connect(self.go_back)

        board.setLayout(layout)
        main_layout.addWidget(board)
        self.setLayout(main_layout)

    def go_to_class(self):
        from ui.screens.study_module_screen import StudyModuleScreen

        screen = StudyModuleScreen(
            self.main_window,
            self.nivel,
            self.modulo,
            0,
            True
        )
        self.main_window.change_screen(screen)

    def go_to_exam(self):
        from ui.screens.module_exam_screen import ModuleExamScreen
        screen = ModuleExamScreen(
            self.main_window,
            self.nivel,
            self.modulo
        )
        self.main_window.change_screen(screen)

    def go_back(self):
        
        self.main_window.open_module_screen(self.nivel)
