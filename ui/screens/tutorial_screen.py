from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from ui.sounds.sound_manager import SoundManager


class TutorialScreen(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Texto de cada página del tutorial
        self.pages = [
            "Bienvenido a MemoKanji.\nEsta aplicación está inspirada en el método de Remembering the Kanji, de James Heisig.\nAquí aprenderás los kanji de uso común, de forma visual y lógica, usando historias y asociaciones que facilitan recordar incluso los símbolos más complejos.\nEsta app no enseña lectura, sino significado y memoria visual, que facilitará el aprendizaje del japones al conocer los significados al agregar las lecturas ya conociendo los significados.",
            "Cada kanji se explica de manera clara:\n• Su forma\n• Su significado\n• Sus “componentes” o partes\n• Una historia o imagen mental para recordarlo.",
            "A partir del tercer nivel deberás crear tus propias historias para recordar los nuevos Kanji.\nPersonalizar el significado hace que el aprendizaje sea mucho más sólido.\nAvanzarás por niveles y módulos, cada uno con un conjunto pequeño y manejable de kanji.",
            "El proceso de estudio sigue siempre la misma secuencia:\nEstudio: lees el kanji, su significado y su historia.\nMnemotecnia: relacionas visualmente el símbolo con una imagen o idea.\nExámenes: al completar un módulo o un nivel, realizas un examen para avanzar.\nEste ciclo asegura que recuerdes cada kanji a largo plazo\n No se recomienda apreder más de dos módulos diarios para no saturarse de información. La fuerza principal de la aplicación se encuentra en la práctica diaria de los kanji y la asociación de las historias o imagenes mentales que relaciones a cada kanji",
            "Modo Práctica: La parte más importante junto con la creación de historias.\n Sigue la misma mecanica que los examenes de módulo y nivel de manera infinita \nRevisión SRS: la aplicación decide qué kanji debes volver a ver según un sistema de repaso inteligente mostrando los kanji más dificiles con frecuencia",
            "Cada vez que completas un módulo o un nivel, tendrás un examen de 10 preguntas.\n• Si apruebas → ganas estrellas y avanzas en tu progreso\n• Si no → puedes volver a estudiar y reintentar\n• Al terminar, verás tus resultados \nUna vez termines el tutorial, comenzarás desde la pantalla principal.\n¡Disfruta el proceso y avanza a tu ritmo!\nVamos a aprender kanji de forma eficiente y sin estrés.",
        ]

        self.index = 0
        self.init_ui()

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
        board_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        board_layout.setContentsMargins(50, 25, 50, 25)
        # board_layout.setSpacing(20)

        # Título
        self.title = QLabel("MemoKanji")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #d4d2d2;")
        board_layout.addWidget(self.title)

        # Flechas como en StudyModuleScreen
        arrow_layout = QHBoxLayout()
        arrow_layout.setSpacing(50)
        arrow_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.left_btn = QPushButton("←")
        self.left_btn.setFixedSize(60, 60)
        self.left_btn.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        self.left_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #d4d2d2;
            }
            QPushButton:hover {
                color: #FFD27F;
            }
            QPushButton:disabled {
                color: #8FA39B;
            }
        """)
        self.left_btn.clicked.connect(self.prev_page)
        self.left_btn.setEnabled(False)
       
       # Texto central
        self.text_label = QLabel(self.pages[self.index])
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.text_label.setFixedSize(600, 500)  

        self.text_label.setWordWrap(True)
        self.text_label.setFont(QFont("Arial", 18))
        self.text_label.setStyleSheet("color: #d4d2d2;")

        self.right_btn = QPushButton("→")
        self.right_btn.setFixedSize(60, 60)
        self.right_btn.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        self.right_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #d4d2d2;
            }
            QPushButton:hover {
                color: #FFD27F;
            }
            QPushButton:disabled {
                color: #8FA39B;
            }
        """)
        self.right_btn.clicked.connect(self.next_page)

        arrow_layout.addWidget(self.left_btn)
        arrow_layout.addWidget(self.text_label)
        arrow_layout.addWidget(self.right_btn)

        board_layout.addLayout(arrow_layout)
        board.setLayout(board_layout)
        main_layout.addWidget(board)

        self.setLayout(main_layout)

    def next_page(self):
        SoundManager.play_click()

        if self.index == len(self.pages) - 1:
            # terminar tutorial
            self.main_window.finish_tutorial()
            return

        self.index += 1
        self.update_page()

    def prev_page(self):
        SoundManager.play_click()

        if self.index > 0:
            self.index -= 1
            self.update_page()

    def update_page(self):
        SoundManager.play_write()
        self.text_label.setText(self.pages[self.index])
        widgets_to_animate = [
            self.text_label
            # self.left_btn , 
            # self.right_btn      
            ]
        from ui.animations.study_switch import animate_screen_entry
        QTimer.singleShot(0, lambda: animate_screen_entry(True, widgets_to_animate))

        self.left_btn.setEnabled(self.index > 0)
        self.right_btn.setEnabled(True)

