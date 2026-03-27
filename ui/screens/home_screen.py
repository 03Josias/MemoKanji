from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel,QHBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from ui.screens.study_screen import StudyScreen
from ui.sounds.sound_manager import SoundManager

class HomeScreen(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Contenedor pizarra
        board = QWidget()
        board.setFixedSize(1000, 650)
        board.setObjectName("board")

        board.setStyleSheet("""
            QWidget#board {
                background-color: #2E6F57;   /* Verde pizarra */
                border: 10px solid #8B5A2B; /* Marco madera */
                border-radius: 8px;
            }
        """)

        board_layout = QVBoxLayout()
        # board_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        board_layout.setContentsMargins(50, 25, 50, 25)
        board_layout.setSpacing(20)
        top_bar = QHBoxLayout()


        #Sound button
        self.sound_button = QPushButton("🔊")
        self.sound_button.setFixedSize(50, 50)
        self.sound_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 22px;
            }
        """)
        self.sound_button.clicked.connect(self.toggle_sound)

        if SoundManager.sound_enabled:
            self.sound_button.setText("🔊")
        else:
            self.sound_button.setText("🔇")

        #Topbar
        top_bar.addStretch()
        top_bar.addWidget(self.sound_button)

        board_layout.addLayout(top_bar)
        board_layout.addStretch(1)        # ← empuja contenido hacia abajo

        # Título
        self.title = QLabel("MemoKanji\n字")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #d4d2d2;")

        board_layout.addWidget(self.title)
        board_layout.addStretch(1)        # ← empuja contenido hacia abajo


        # Botón Estudiar
        self.study_button = self.create_menu_button("ESTUDIAR")
        self.study_button.clicked.connect(self.go_to_study)

        # Botón Practicar
        self.practice_button = self.create_menu_button("PRACTICAR")
        self.practice_button.clicked.connect(self.go_to_practice)

        board_layout.addWidget(self.study_button, alignment=Qt.AlignmentFlag.AlignCenter)
        board_layout.addSpacing(20)
        board_layout.addWidget(self.practice_button, alignment=Qt.AlignmentFlag.AlignCenter)
        board_layout.addStretch(2)        # ← empuja contenido hacia arriba
        board.setLayout(board_layout)


        layout.addWidget(board, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        from ui.animations.hover_animation import apply_hover_scale
        apply_hover_scale(self.study_button)
        apply_hover_scale(self.practice_button)

    def create_menu_button(self, text):

        button = QPushButton(text)
        button.setFixedSize(350, 80)
        button.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        button.setStyleSheet("""
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
        
        button.clicked.connect(SoundManager.play_click)

        return button

    def go_to_study(self):
        screen=StudyScreen(self.main_window)
        self.main_window.change_screen(screen,keep_current=True)

    def go_to_practice(self):
        screen=self.start()
        self.main_window.change_screen(screen,keep_current=True)

    def start(self):
        if not self.main_window.practice_service.check_open():
            from ui.widgets.practice_aviso import PracticeAviso
            aviso = PracticeAviso(self.main_window)
            return aviso
        else:
            from ui.screens.practice_screen import PracticeScreen
            screen = PracticeScreen(self.main_window)
            return screen

    def toggle_sound(self):
        SoundManager.toggle_sound()

        if SoundManager.sound_enabled:
            self.sound_button.setText("🔊")
        else:
            self.sound_button.setText("🔇")