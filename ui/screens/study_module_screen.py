
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtCore import QParallelAnimationGroup, QSequentialAnimationGroup

from models.kanji import Kanji
from models.radical import Radical
from ui.widgets.radical_introduction import RadicalIntroduction
from ui.widgets.back_button import BackButton
from services.LimitedTextEdit import LimitedTextEdit
from ui.sounds.sound_manager import SoundManager

BASE=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 319, 1070, 1105, 1251]

class StudyModuleScreen(QWidget):

    def __init__(self, main_window, nivel, modulo,current_index,direction):
        super().__init__()

        self.main_window = main_window
        self.session = main_window.session

        self.nivel = nivel
        self.modulo = modulo

        self.kanjis = self.get_kanjis()
        self.current_index = current_index
        self.direction=direction
        self.radicales=self.get_radicales()

        self.init_ui()
        self.update_kanji_display()

    def get_kanjis(self):
        return (
            self.session.query(Kanji)
            .filter_by(nivel=self.nivel, modulo=self.modulo)
            .order_by(Kanji.orden_en_modulo)
            .all()
        )
    def get_radicales(self):
        radicales=self.session.query(Radical).order_by(Radical.orden).all()
        radicales_orden=[]
        for radical in radicales:
            radicales_orden.append(radical.orden)
        return radicales_orden

    def init_ui(self):
        te="bien, dame el código para hacer el cambio para que se vea como en la imagen primer imagen (con los botones al costado del kanji), r simplemente als flechas pintadas en el pizarron bien, dame el código para hacer el cambio para que se vea como en la imagen primer imagen (con los botones al costado del kanji), pero elimina el circulo al rededor del boton, debe ser simplemente als flechas pintadas en el pizarron pero elimina el pero para cuando tu mama rimer imagen con los botones al costado del kanji), pero elimina el circulo al rededo rimer imagen popo(  con los botones al costado del kanji), pero elimina el circulo al rededo rimer imagen popo(  con los botones"
        print("/////////////////////////////////////////////")
        #caracteres en te
        print(len(te))
        print("/////////////////////////////////////////////")
        print("/////////////////////////////////////////////")

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
        board_layout.setSpacing(20)

        # Barra superior
        top_bar = QHBoxLayout()
        back_button = BackButton()
        back_button.clicked.connect(self.go_back)

        top_bar.addWidget(back_button)
        top_bar.addStretch()

        board_layout.addLayout(top_bar)

        # Título
        self.title = QLabel(f"Nivel {self.nivel} - Módulo {self.modulo}")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #d4d2d2;")
        board_layout.addWidget(self.title)

        # Contenedor horizontal para flechas + kanji
        kanji_row = QHBoxLayout()
        kanji_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        kanji_row.setSpacing(200)

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
        self.prev_button.clicked.connect(self.show_previous_kanji)

        # Kanji grande
        self.kanji_label = QLabel("")
        self.kanji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.kanji_label.setFont(QFont("Arial", 120))
        self.kanji_label.setStyleSheet("color: #d4d2d2;")

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
        self.next_button.clicked.connect(self.show_next_kanji)
        kanji_row.addWidget(self.prev_button)
        kanji_row.addWidget(self.kanji_label)
        kanji_row.addWidget(self.next_button)
        board_layout.addLayout(kanji_row)
        
        # Significado
        self.meaning_label = QLabel("")
        self.meaning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.meaning_label.setFont(QFont("Arial", 20))
        self.meaning_label.setStyleSheet("color: #d4d2d2;")
        board_layout.addWidget(self.meaning_label)
         
        # Pistas
        self.clue_label = QLabel("")
        self.clue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clue_label.setFont(QFont("Arial", 14))
        self.clue_label.setStyleSheet("color: #d4d2d2;")
        board_layout.addWidget(self.clue_label)
        self.clue_label.hide()

        # Contenedor para la historia (debajo del kanji)
        story_container = QWidget()
        story_layout = QVBoxLayout()
        story_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        story_layout.setSpacing(10)
        story_layout.setContentsMargins(50, 10, 50, 10)

        # Label para mostrar historia (solo lectura)
        self.story_label = QLabel("")
        self.story_label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.story_label.setFont(QFont("Arial", 12))
        self.story_label.setStyleSheet("color: #E6D5B8;")
        self.story_label.setWordWrap(True)
        self.story_label.setFixedSize(800,150)
        story_layout.addWidget(self.story_label)

        # Área edicion historia
        self.story_input = LimitedTextEdit()
        self.story_input.setFixedHeight(100)
        self.story_input.setFont(QFont("Arial", 14))
        self.story_input.setStyleSheet("""
            QTextEdit {
                background-color: #2E6F57;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        self.story_input.hide()
        story_layout.addWidget(self.story_input)

        # Botón de editar/guardar (inicialmente oculto)
        self.edit_button = QPushButton("✏️")
        self.edit_button.setFixedSize(40, 40)
        self.edit_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #2E6F57;
                border-radius: 8px;
                color: black;
            }
            QPushButton:hover {
                background-color: #1f4f3e;
            }
        """)
        self.edit_button.clicked.connect(self.toggle_edit_mode)
        self.edit_button.hide()

        story_layout.addWidget(self.edit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        #Botón examen
        self.open_exam_button = QPushButton("Examen")
        self.open_exam_button.setFixedSize(200, 60)
        self.open_exam_button.setFont(QFont("arial", 16, QFont.Weight.Bold))
        self.open_exam_button.setStyleSheet("""
            QPushButton {
                background-color: #27634d;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #1f4f3e;
            }
        """)
        self.open_exam_button.clicked.connect(SoundManager.play_click)
        self.open_exam_button.clicked.connect(self.open_exam)

        from ui.animations.hover_animation import apply_hover_scale
        apply_hover_scale(self.open_exam_button)
        
        story_container.setLayout(story_layout)
        board_layout.addWidget(story_container)
        board_layout.addWidget(self.open_exam_button, alignment=Qt.AlignmentFlag.AlignCenter)

        board.setLayout(board_layout)
        main_layout.addWidget(board)

        self.setLayout(main_layout)

    def load_kanji(self):

        kanji = self.kanjis[self.current_index]

        self.kanji_label.setText(kanji.caracter)
        self.meaning_label.setText(f"Significado: {kanji.significado}")

        self.update_story_display()

        kanji.visto = True
        self.session.commit()

    def update_story_display(self):
        """Actualiza la visualización de la historia según el estado"""
        kanji = self.kanjis[self.current_index]

        tiene_historia_nb = kanji.historia and kanji.historia.strip() != "penidente" and kanji.orden_global not in BASE
        # self.story_input.blockSignals(False)
        es_base=kanji.historia and kanji.orden_global in BASE
        # Ocultar todo primero
        self.story_label.hide()
        self.story_input.hide()
        self.edit_button.hide()
        self.clue_label.hide()
    
        if es_base:
            # Kanji base: mostrar historia fija
            self.story_label.setText(f"Historia: {kanji.historia}")
            self.story_label.show()
        
        elif tiene_historia_nb:
            # Tiene historia personalizada: mostrarla con opción de editar
            self.story_label.setText(f"Historia: {kanji.historia}")
            self.story_label.show()
            self.edit_button.setText("✏️")
            self.edit_button.show()
        
        else:
            # No tiene historia: mostrar pistas e input para crear
            self.clue_label.setText(kanji.pista)
            self.clue_label.show()
            self.story_input.setPlaceholderText("Escribe tu propia historia para recordar este kanji...")
            self.story_input.setText("")
            self.story_input.show()
            self.edit_button.setText("📝")
            self.edit_button.show()

    def toggle_edit_mode(self):
        """Cambia entre modo ver y modo editar"""
        kanji = self.kanjis[self.current_index]
        max_caracteres = 668
    
        if self.story_input.isVisible():
            # Guardar historia
            nueva_historia = self.story_input.toPlainText().strip()
            if nueva_historia:
                kanji.historia = nueva_historia
                self.session.commit()
                self.update_story_display()
        else:
            # Entrar modo edición
            self.story_input.setText(kanji.historia)
            self.story_label.hide()
            self.story_input.show()
            self.edit_button.setText("📝")

    def update_kanji_display(self):
        kanji = self.kanjis[self.current_index]
        # Guardar historia actual si está en edición
        if hasattr(self, 'kanji') and kanji:
            kanji = kanji
            if kanji.orden_global > 100 and self.story_input.isVisible():
                historia_nueva = self.story_input.toPlainText().strip()
                if historia_nueva:
                    kanji.historia = historia_nueva
                    self.session.commit()

        self.load_kanji()

        widgets_to_animate = [
            self.kanji_label,      # kanji
            self.meaning_label , 
            self.clue_label,          
            self.story_label if self.story_label.isVisible() else self.story_input
            ]
        from ui.animations.study_switch import animate_screen_entry
        QTimer.singleShot(0, lambda: animate_screen_entry(self.direction, widgets_to_animate))
        
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.kanjis) - 1)
        self.is_complete()

    def show_next_kanji(self):
        self.direction=True
        kanji = self.kanjis[self.current_index]
        if kanji.orden_global in self.radicales:
            self.show_radical(kanji)
            return
        if self.current_index < len(self.kanjis) - 1:
            self.current_index += 1
            self.update_kanji_display()

    def show_previous_kanji(self):
        self.direction=False

        kanji=self.kanjis[self.current_index]
        if kanji.orden_global-1 in self.radicales:
            self.show_radical(kanji)
            return

        if self.current_index > 0:
            # Guardar historia actual si está en edición
            if hasattr(self, 'current_kanji') and self.kanji:
                kanji = self.kanji
                if kanji.orden_global > 100 and self.story_input.isVisible():
                    historia_nueva = self.story_input.toPlainText().strip()
                    if historia_nueva:
                        kanji.historia = historia_nueva
                        self.session.commit()
        
            self.current_index -= 1
            self.update_kanji_display()

    def is_complete(self):

        if all(k.visto for k in self.kanjis):
            self.open_exam_button.setEnabled(True)
        else:
            self.open_exam_button.setEnabled(False)

    def show_radical(self,kanji):
        is_completed=all(k.visto for k in self.kanjis)
        if not self.direction:
            orden=kanji.orden_global-1
            
        else:
            orden=kanji.orden_global            

        screen=RadicalIntroduction(
                self.main_window,
                self.nivel,
                self.modulo, 
                orden, 
                self.current_index,
                is_completed,
                self.direction
                )
        self.main_window.change_screen(screen)

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
        
