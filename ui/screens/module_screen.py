
from tkinter import BUTT, Button
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from models import kanji
from models.progreso import ModuloProgreso, NivelProgreso
from ui.widgets.back_button import BackButton
from ui.screens.study_module_screen import StudyModuleScreen
from ui.widgets.module_button import ModuleButtonWidget
from ui.widgets.level_exam_button import LevelExamButtonWidget
from ui.screens.study_screen import StudyScreen

class ModuleScreen(QWidget):

    def __init__(self, main_window, nivel):
        super().__init__()

        self.main_window = main_window
        self.session = main_window.session
        self.nivel = nivel
        self.level_exam_button = None
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Pizarra
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
        board_layout.setSpacing(50)
        board_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        board_layout.setContentsMargins(50, 25, 50, 25)

        # Barra superior
        top_bar = QHBoxLayout()

        back_button = BackButton()
        back_button.clicked.connect(self.go_back)

        self.table_button = QPushButton("📋 Kanji")
        self.table_button.setFixedSize(140, 40)
        self.table_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.table_button.clicked.connect(self.open_kanji_table)
        
        from ui.animations.hover_animation import apply_hover_scale
        apply_hover_scale(self.table_button)
        top_bar.addWidget(back_button)
        top_bar.addStretch()
        top_bar.addWidget(self.table_button)

        board_layout.addLayout(top_bar)

        # Título
        title = QLabel(f"Nivel {self.nivel}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #d4d2d2;")

        board_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop)


        # Grid módulos
        self.grid = QGridLayout()
        self.grid.setSpacing(30)
        self.grid.setContentsMargins(25, 25, 25, 25)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        #Crear boton exmen
        self.level_exam_button = self.create_level_exam_button()

        self.create_module_grid()
        board_layout.addLayout(self.grid)

        board.setLayout(board_layout)
        main_layout.addWidget(board)
        self.setLayout(main_layout)

        from ui.animations.grid_animation import animate_grid_items

        #QTimer.singleShot(50, lambda: animate_grid_items(self.grid))
        timer = QTimer(board)  # ← board como parent
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: animate_grid_items(self.grid))
        timer.start(0)

        board_layout.addWidget(
            self.level_exam_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )


# VOLVER ATRAS
    def go_back(self):

        study_screen=StudyScreen(self.main_window)
        self.main_window.change_screen(study_screen)

# ABRIR TABLA DE KANJI
    def open_kanji_table(self):
        from ui.widgets.kanji_table import KanjiTable
        kanji_table = KanjiTable(
            self.main_window,
            self.session,
            self.nivel
        )
        self.main_window.change_screen(kanji_table)

# CREAR GID DE MODULOS
    def create_module_grid(self):

        # Limpiar grid
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        modulos = self.get_modulos()

        row = 0
        col = 0

        for modulo in modulos:

            button = self.create_module_button(modulo)

            self.grid.addWidget(
                button,
                row,
                col,
                alignment=Qt.AlignmentFlag.AlignCenter
            )

            col += 1
            if col == 5:
                col = 0
                row += 1
        self.level_exam_button.update_style()
        

# OBTENER MODULOS DEL NIVEL
    def get_modulos(self):
        return (
            self.session.query(ModuloProgreso)
            .filter_by(nivel=self.nivel)
            .order_by(ModuloProgreso.modulo)
            .all()
        )

# CREAR BOTON DE MODULO
    def create_module_button(self, modulo):

        progreso = (
            self.session.query(ModuloProgreso)
            .filter_by(nivel=self.nivel, modulo=modulo.modulo)
            .first()
        )

        button = ModuleButtonWidget(
            self.nivel,
            modulo,
            progreso
        )

        button.clicked.connect(
            lambda m=modulo, p=progreso:
            self.handle_module_click(modulo, progreso)
        )

        return button

# CREAR BOTON DE EXAMEN DE NIVEL
    def create_level_exam_button(self):
        modulos= self.get_modulos()
        progreso= (
            self.session.query(NivelProgreso)
            .filter_by(nivel=self.nivel)
            .first()
            )
        button = LevelExamButtonWidget(
            self.nivel,
            modulos,
            progreso
        )
        button.clicked.connect(
            self.handle_click_level_exam_button
        )
        return button

# ABRIR PANTALLA DE ESTUDIO DE MODULO
    def open_module(self, modulo):
        screen = StudyModuleScreen(
                self.main_window,
                self.nivel,
                modulo,
                current_index=0,
                direction=True
            )
        self.main_window.change_screen(screen)
        
# MANEJAR CLICK EN MODULO
    def handle_module_click(self, modulo, progreso):

        if not progreso.desbloqueado:
            return

        if progreso.completado:
            from ui.widgets.module_options import ModuleOptionsScreen

            screen = ModuleOptionsScreen(
                self.main_window,
                self.nivel,
                modulo.modulo
            )
            self.main_window.change_screen(screen)
        else:
            self.open_module(modulo.modulo)


# ABRIR PANTALLA DE EXAMEN DE MODULO
    def open_exam(self, modulo):
        from ui.screens.module_exam_screen import ModuleExamScreen
        screen = ModuleExamScreen(
            self.main_window,
            self.nivel,
            modulo
        )
        self.main_window.change_screen(screen)

# MANEJAR CLICK EN BOTON DE EXAMEN DE NIVEL
    def handle_click_level_exam_button(self):
        
        if self.main_window.exam_service.all_modules_completed(self.nivel):
            self.open_level_exam()


# ABRIR PANTALLA DE EXAMEN DE NIVEL
    def open_level_exam(self):
        from ui.screens.level_exam_screen import LevelExamScreen
        screen = LevelExamScreen(
            self.main_window,
            self.nivel,
        )
        self.main_window.change_screen(screen)
