


from tkinter import SEL
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


from models.radical import Radical
from ui.widgets.back_button import BackButton
from ui.sounds.sound_manager import SoundManager

class RadicalIntroduction(QWidget):

    def __init__(self, main_window, nivel, modulo, orden_global, current_index, is_completed, direction):
        super().__init__()

        self.main_window = main_window
        self.session = main_window.session

        self.nivel=nivel
        self.modulo=modulo
        self.orden_global=orden_global
        self.current_index=current_index
        self.completed=is_completed
        self.direction=direction
        self.radicales = self.get_radicales()

        if not self.direction:
            self.radical_index=len(self.radicales)-1
        else:
            self.radical_index=0

        self.init_ui()
        self.update_radical_display()

    def get_radicales(self):
        return (
            self.session.query(Radical)
            .filter_by(orden=self.orden_global)
            .all()
        )

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
        board_layout.setSpacing(20)
        board_layout.setContentsMargins(50, 25, 50, 25)

        # Barra superior
        top_bar = QHBoxLayout()
        back_button = BackButton()
        back_button.clicked.connect(self.go_back)

        top_bar.addWidget(back_button)
        top_bar.addStretch()

        board_layout.addLayout(top_bar)

        # Título
        self.title = QLabel(f"Nuevo Componente")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #d4d2d2;")
        board_layout.addWidget(self.title)

        # Contenedor horizontal para flechas + kanji
        radical_row = QHBoxLayout()
        radical_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        radical_row.setSpacing(200)

        # Flecha izquierda
        self.prev_button = QPushButton("←")
        self.prev_button.setFixedSize(60, 60)
        self.prev_button.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        self.prev_button.setStyleSheet("""
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
        self.prev_button.clicked.connect(SoundManager.play_write)
        self.prev_button.clicked.connect(self.show_previous)

        # Radical grande
        self.radical_label = QLabel("")
        self.radical_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.radical_label.setFont(QFont("Arial", 120))
        self.radical_label.setStyleSheet("color: #d4d2d2;")

        # Flecha derecha
        self.next_button = QPushButton("→")
        self.next_button.setFixedSize(60, 60)
        self.next_button.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        self.next_button.setStyleSheet("""
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
        self.next_button.clicked.connect(SoundManager.play_write)
        self.next_button.clicked.connect(self.show_next)

        radical_row.addWidget(self.prev_button)
        radical_row.addWidget(self.radical_label)
        radical_row.addWidget(self.next_button)
        board_layout.addLayout(radical_row)
        
        # Nombre
        self.name_label = QLabel("")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setFont(QFont("Arial", 20))
        self.name_label.setStyleSheet("color: #d4d2d2;")
        board_layout.addWidget(self.name_label)

        #Contenedor para la historia (debajo del kanji)
        explanation_container = QWidget()
        explanation_layout = QVBoxLayout()
        explanation_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        explanation_layout.setSpacing(10)
        explanation_layout.setContentsMargins(50, 10, 50, 10)

        # Label para mostrar historia (solo lectura)
        self.explanation_label = QLabel("")
        self.explanation_label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.explanation_label.setFont(QFont("Arial", 12))
        self.explanation_label.setStyleSheet("color: #E6D5B8;")
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setFixedSize(800,150)
        explanation_layout.addWidget(self.explanation_label)

        #Botón examen
        self.open_exam_button = QPushButton("Examen")
        self.open_exam_button.setFixedSize(200, 60)
        self.open_exam_button.setFont(QFont("arial", 16, QFont.Weight.Bold))
        self.open_exam_button.setStyleSheet("""
            QPushButton {
                background-color: #27634d;
                border-radius: 15px;
                color: #d4d2d2;
            }
            QPushButton:hover {
                background-color: #1f4f3e;
            }
        """)
        
        self.open_exam_button.clicked.connect(SoundManager.play_click)

        self.open_exam_button.clicked.connect(self.open_exam)

        explanation_container.setLayout(explanation_layout)
        board_layout.addWidget(explanation_container)
        board_layout.addWidget(self.open_exam_button, alignment=Qt.AlignmentFlag.AlignCenter)

        board.setLayout(board_layout)
        main_layout.addWidget(board)

        self.setLayout(main_layout)

    def load_radical(self,radical):

        self.radical_label.setText(radical.simbolo)
        self.name_label.setText(f"Nombre: {radical.nombre}")

        self.update_explanation_display(radical)

        self.session.commit()

    def update_explanation_display(self,radical):
        """Actualiza la visualización de la historia según el estado"""

        self.explanation_label.setText(f"Explicación: {radical.explicacion}")

            #self.explanation_label.show()
        
    def update_radical_display(self):
        print("indice show previo")
        print(self.radical_index)

        radical=self.radicales[self.radical_index]
        
        print(radical)
        self.load_radical(radical)

        widgets_to_animate = [
            self.radical_label,    
            self.name_label,    
            self.explanation_label
            ]
        from ui.animations.study_switch import animate_screen_entry
        QTimer.singleShot(0, lambda: animate_screen_entry(self.direction,widgets_to_animate))
        
        self.prev_button.setEnabled(self.current_index >=0)
        self.next_button.setEnabled(self.current_index <= 9)
        self.is_completed()

    def show_next(self):
        if self.direction==False:
            self.radical_index=len(self.radicales)-1

        if self.radical_index==len(self.radicales)-1 and self.current_index < 9:
            from ui.screens.study_module_screen import StudyModuleScreen
            if self.direction:
                self.current_index+=1
            #self.direction=True
            next_kanji= StudyModuleScreen(
                self.main_window,
                self.nivel,
                self.modulo,
                self.current_index,
                direction=True
                )
            self.main_window.change_screen(next_kanji)
            return
        else:
            self.radical_index+=1
            self.update_radical_display()

    def show_previous(self):
        if self.radical_index==0:
            if self.current_index>0:
                if not self.direction:
                    self.current_index-=1
                
            from ui.screens.study_module_screen import StudyModuleScreen
            print("********************************************************")
            print(f"CURRENT INDEX: {self.current_index}")
            print("********************************************************")
            print("********************************************************")
            #self.direction=False
            prev_kanji=StudyModuleScreen(
                self.main_window,
                self.nivel,
                self.modulo,
                self.current_index,
                direction=False
                )
            self.main_window.change_screen(prev_kanji)
            return
        if self.radical_index>0:
            print("indice show previo")
            print(self.radical_index)
            self.radical_index-=1
            print("indice show actual")
            print(self.radical_index)
            self.update_radical_display()
    
    def is_completed(self):

        if self.completed:
            self.open_exam_button.setEnabled(True)
        else:
            self.open_exam_button.setEnabled(False)

    def open_exam(self):

        from ui.screens.module_exam_screen import ModuleExamScreen

        screen = ModuleExamScreen(
            self.main_window,
            self.nivel,
            self.modulo
            )
        self.main_window.change_screen(screen)

    def go_back(self):

        self.main_window.open_module_screen(self.nivel)
