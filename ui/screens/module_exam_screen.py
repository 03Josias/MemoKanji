from turtle import right
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from ui.widgets.back_button import BackButton
from ui.sounds.sound_manager import SoundManager
from ui.animations.kanji_fade_animation import fade_scale_widget


class ModuleExamScreen(QWidget):

    def __init__(self, main_window, nivel, modulo):
        super().__init__()

        self.main_window = main_window
        self.session = main_window.session
        self.exam_service = main_window.exam_service

        self.nivel = nivel
        self.modulo = modulo
        self.current_kanji=None
        self.questions = self.exam_service.generate_module_exam(
            nivel, modulo
        )

        self.init_ui()
        # self.load_question()
        QTimer.singleShot(50, self.load_question)

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        board = QWidget()
        board.setObjectName("board")
        board.setFixedSize(1000, 650)

        board.setStyleSheet("""
            QWidget#board {
                background-color: #2E6F57;
                border: 10px solid #8B5A2B;
                border-radius: 8px;
            }
        """)

        board_layout = QVBoxLayout()
        # board_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        board_layout.setContentsMargins(50, 25, 50, 25)
        board_layout.setSpacing(30)
       # Barra superior
        top_bar = QHBoxLayout()
        back_button = BackButton()
        back_button.clicked.connect(self.go_back)

        # Progreso
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setFont(QFont("Arial", 16))
        self.progress_label.setStyleSheet("color: #d4d2d2;")
        #board_layout.addWidget(self.progress_label)

        top_bar.addWidget(back_button)
        top_bar.addStretch()
        top_bar.addWidget(self.progress_label)
        top_bar.addSpacing(20)

        board_layout.addLayout(top_bar)

        # Título
        self.title = QLabel(
            f"Examen Nivel {self.nivel} - Módulo {self.modulo}"
        )
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #d4d2d2;")
        board_layout.addWidget(self.title)
        board_layout.addStretch()  # ← empuja todo hacia arriba

        #Significado grande
        self.meaning_label = QLabel("")
        self.meaning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.meaning_label.setFont(QFont("Arial", 35, QFont.Weight.Bold))  # Tamaño grande para el significado
        self.meaning_label.setStyleSheet("color: #d4d2d2;")
        self.meaning_label.setWordWrap(True)  # Por si el significado es largo
        board_layout.addWidget(self.meaning_label)
        board_layout.addStretch()  # ← empuja todo hacia arriba

         # Contenedor para los botones en grid 2x2
        buttons_container = QWidget()
        buttons_grid = QGridLayout(buttons_container)
        buttons_grid.setSpacing(10)  # Espacio entre botones
        buttons_grid.setContentsMargins(20, 5, 20, 5)

        # Opciones
        self.option_buttons = []

        for _ in range(4):
            btn = QPushButton("")
            btn.setFixedSize(120, 120)
            btn.setFont(QFont("Arial", 60, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                background-color: #3A7761;
                border-radius: 18px;
                color:#d4d2d2;
                }
                QPushButton:hover {
                    background-color: #316351;
                }
                QPushButton:pressed {
                    background-color: #285243;
                }
        """)
            btn.clicked.connect(self.check_answer)
            self.option_buttons.append(btn)

            from ui.animations.hover_animation import apply_hover_scale
            apply_hover_scale(btn)

        buttons_grid.addWidget(self.option_buttons[0], 0, 0)  
        buttons_grid.addWidget(self.option_buttons[1], 0, 1)  
        buttons_grid.addWidget(self.option_buttons[2], 1, 0)  
        buttons_grid.addWidget(self.option_buttons[3], 1, 1)  

        board_layout.addWidget(buttons_container, alignment=Qt.AlignmentFlag.AlignHCenter)


        board.setLayout(board_layout)
        main_layout.addWidget(board)

        self.setLayout(main_layout)
        
    def load_question(self):

        self.progress_label.setText(f"Pregunta {self.exam_service.current_index + 1} / 10    |    Errores: {self.exam_service.errors} / 4")
        
        if not self.exam_service.module_exam_active():
            self.finish_exam()
            return

        kanji = self.questions[self.exam_service.current_index]
        self.current_kanji = kanji

        fade_scale_widget(self.meaning_label,kanji.significado)

        # Generar opciones
        all_kanji = self.session.query(type(kanji)).all()
        caracter = [k.caracter for k in all_kanji]

        import random

        wrong = random.sample(
            [m for m in caracter if m != kanji.caracter],
            3
        )

        options = wrong + [kanji.caracter]
        random.shuffle(options)

        for btn, text in zip(self.option_buttons, options):
            btn.setText(text)
            fade_scale_widget(btn, text)
            btn.setEnabled(True)


    def check_answer(self):

        selected_button = self.sender()
        selected_text = selected_button.text()

        correct = self.exam_service.evaluate_module_answer(
            self.current_kanji,
            selected_text
        )

        # Desactivar todos los botones temporalmente
        right_btn=self.get_right_button()
        for btn in self.option_buttons:
            btn.setEnabled(False)
            if btn != right_btn and btn != selected_button:
                btn.setStyleSheet("""
                QPushButton {
                    background-color: #346153;
                    
                    border-radius: 18px;
                    color:#d4d2d2;
                    }
                """)

        # Colorear botón
        if correct:
            SoundManager.play_correct()

            selected_button.setStyleSheet("""
                QPushButton {
                    background-color: #02b072;
                    border-radius: 15px;
                    color: #d4d2d2
                }
            """)
        else:
            from ui.animations.shake_animation import apply_shake
            apply_shake(selected_button)

            right_btn.setStyleSheet("""
                QPushButton {
                    background-color: #02b072;
                    border-radius: 15px;
                    color: #d4d2d2
            }
            """)
            SoundManager.play_wrong()
            selected_button.setStyleSheet("""
                QPushButton {
                    background-color: #a14549;
                    border-radius: 15px;
                    color: #d4d2d2
                }
            """)

        # Esperar 700ms antes de continuar
        QTimer.singleShot(200, self.next_step)

    def get_right_button(self):
        for btn in self.option_buttons:
            if btn.text()==self.current_kanji.caracter:
                return btn

    def next_step(self):

        # Restaurar estilo original
        for btn in self.option_buttons:
            btn.setStyleSheet("""
                QPushButton {
                background-color: #3A7761;
                border-radius: 18px;
                color:#d4d2d2;
                }
                QPushButton:hover {
                    background-color: #316351;
                }
                QPushButton:pressed {
                    background-color: #285243;
                }
        """)

        if not self.exam_service.module_exam_active():
            self.finish_exam()
        else:
            self.load_question()

    def finish_exam(self):

        passed = self.exam_service.module_passed()
        correct = self.exam_service.correct_answers
        stars = self.exam_service.calculate_stars()


        if passed:
            self.exam_service.complete_module(
                self.nivel,
                self.modulo
            )
        self.exam_service.update_level_stars(self.nivel)

        from ui.screens.exam_result_screen import ExamResultScreen

        screen = ExamResultScreen(
            self.main_window,
            self.nivel,
            self.modulo,
            passed,
            correct,
            stars
        )
        self.main_window.change_screen(screen)

    def go_back(self):
        self.main_window.open_module_screen(self.nivel)
