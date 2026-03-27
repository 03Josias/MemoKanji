import random

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from services.practice_service import PracticeService
from models.kanji import Kanji
from ui.widgets.back_button import BackButton
from ui.sounds.sound_manager import SoundManager
from ui.animations.kanji_fade_animation import fade_scale_widget

class PracticeScreen(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.session = main_window.session
        self.practice_service = main_window.practice_service                
        self.current_kanji = None

        self.init_ui()
        #self.load_question()
        QTimer.singleShot(50, self.load_question)

    # ===============================
    # UI
    # ===============================

    def init_ui(self):
        self.practice_service.reset_practice()
        
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Pizarra ---
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

        board_layout = QVBoxLayout()
        board_layout.setContentsMargins(50, 25, 50, 25)
        board_layout.setSpacing(30)

        # Barra superior
        top_bar = QHBoxLayout()

        back_button = BackButton()
        back_button.clicked.connect(self.go_back)

        self.streak_label = QLabel("Racha: 0")
        self.streak_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.streak_label.setStyleSheet("color: #d4d2d2;")

        self.error_label = QLabel("Errores: 0 / 3")
        self.error_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.error_label.setStyleSheet("color: #d4d2d2;")

        top_bar.addWidget(back_button)
        top_bar.addStretch()
        top_bar.addWidget(self.streak_label)
        top_bar.addSpacing(20)
        top_bar.addWidget(self.error_label)

        board_layout.addLayout(top_bar)

        # Significado grande (en lugar de kanji)
        self.meaning_label = QLabel("")
        self.meaning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.meaning_label.setFont(QFont("Arial", 40, QFont.Weight.Bold))  # Tamaño grande para el significado
        self.meaning_label.setStyleSheet("color: #d4d2d2;")
        self.meaning_label.setWordWrap(True)  # Por si el significado es largo
        board_layout.addWidget(self.meaning_label)
        # Pistas
        self.clue_label = QLabel("")
        self.clue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clue_label.setFont(QFont("Arial", 14))
        self.clue_label.setStyleSheet("color: #d4d2d2;")
        board_layout.addWidget(self.clue_label)

        # Contenedor para los botones en grid 2x2
        buttons_container = QWidget()
        buttons_grid = QGridLayout(buttons_container)
        buttons_grid.setSpacing(10)  # Espacio entre botones
        buttons_grid.setContentsMargins(20, 5, 20, 5)

        # Opciones
        self.option_buttons = []

        for i in range(4):
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
                    background-color: #285243

                }
        """)
            btn.clicked.connect(self.check_answer)

            self.option_buttons.append(btn)

            from ui.animations.hover_animation import apply_hover_scale
            apply_hover_scale(btn,scale=1.08)

        buttons_grid.addWidget(self.option_buttons[0], 0, 0)  
        buttons_grid.addWidget(self.option_buttons[1], 0, 1)  
        buttons_grid.addWidget(self.option_buttons[2], 1, 0)  
        buttons_grid.addWidget(self.option_buttons[3], 1, 1)  

        board_layout.addWidget(buttons_container, alignment=Qt.AlignmentFlag.AlignCenter)

        board.setLayout(board_layout)
        main_layout.addWidget(board)

        self.setLayout(main_layout)

    # ===============================
    # Lógica práctica
    # ===============================
    
    def load_question(self):

        if not self.practice_service.practice_active():
            self.finish_practice()
            return

        kanji = self.practice_service.get_weighted_random_kanji()

        if not kanji:
            self.finish_practice(no_more=True)
            return

        self.current_kanji = kanji

        #self.meaning_label.setText(kanji.significado)
        fade_scale_widget(self.meaning_label, kanji.significado)

        fade_scale_widget(self.clue_label,kanji.pista)
        
        #self.kanji_label.setText(kanji.caracter)

        all_seen = self.practice_service.get_available_kanji()

        wrong_options = random.sample(
            [k.caracter for k in all_seen if k.id != kanji.id],
            3
        )
        
        options = wrong_options + [kanji.caracter]

        random.shuffle(options)
        
        for btn, text in zip(self.option_buttons, options):
            btn.setText(text)
            fade_scale_widget(btn, text)
            btn.setEnabled(True)
        
        print(f"""
        Intervalo: {self.current_kanji.intervalo:.2f}
        Facilidad: {self.current_kanji.facilidad:.2f}
        Reps: {self.current_kanji.repeticiones}""")

    def check_answer(self):
        if hasattr(self, "_answer_locked") and self._answer_locked:
            return

        self._answer_locked = True

        selected_button = self.sender()
        selected_text = selected_button.text()

        correct = self.practice_service.evaluate_answer(
            self.current_kanji,
            selected_text
        )

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
                #2e5448
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
            SoundManager.play_wrong()
            right_btn.setStyleSheet("""
            QPushButton {
                background-color: #02b072;
                border-radius: 15px;
                color: #d4d2d2
                }
            """)

            selected_button.setStyleSheet("""
                QPushButton {
                    background-color: #a14549;
                    border-radius: 15px;
                    color: #d4d2d2
                }
            """)
            # besto b04f53
        self.update_indicators()

        QTimer.singleShot(300, self.next_step)
    
    def get_right_button(self):
        for btn in self.option_buttons:
            if btn.text() == self.current_kanji.caracter:
                return btn

    def next_step(self):
        SoundManager.stop_all()
        # Restaurar estilo original
        for btn in self.option_buttons:
            btn.setFixedSize(120, 120)
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
        self._answer_locked = False
        if not self.practice_service.practice_active():

            self.finish_practice()
        else:
            self.load_question()

    def update_indicators(self):
        self.streak_label.setText(
            f"Racha: {self.practice_service.current_streak}"
        )
        self.error_label.setText(
            f"Errores: {self.practice_service.errors} / 3"
        )

    # ===============================
    # Finalización
    # ===============================

    def finish_practice(self, no_more=False):
        
        total_seen = self.session.query(Kanji).filter_by(visto=True).count()

        all_kanji = self.session.query(Kanji).count()

        
        from ui.screens.practice_result_screen import PracticeResultScreen

        screen = PracticeResultScreen(
            self.main_window,
            self.practice_service.current_streak,
            self.practice_service.max_streak,
            total_seen,
            all_kanji,
            no_more

        )
        self.main_window.change_screen(screen)

    def go_back(self):
        self.main_window.navigate_to(self.main_window.home_screen)
