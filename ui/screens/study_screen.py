
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGridLayout, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from models.progreso import NivelProgreso
from ui import main_window
from ui.widgets.back_button import BackButton
from ui.widgets.level_button import LevelButtonWidget
from ui.animations.hover_animation import apply_hover_scale

class StudyScreen(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.session = main_window.session

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # PIZARRA
        board = QWidget()
        board.setMinimumSize(1000, 650)
        board.setObjectName("board")

        board.setStyleSheet("""
            QWidget#board {
                background-color: #2E6F57;
                border: 10px  solid #8B5A2B;
                border-radius: 8px;
            }
        """)

        board_layout = QVBoxLayout()
        board_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        board_layout.setContentsMargins(50, 25, 50, 25)
        board_layout.setSpacing(10)


        # Botón volver
        back_button = BackButton()
        back_button.clicked.connect(self.go_back)

        top_bar = QHBoxLayout()
        top_bar.addWidget(back_button)
        top_bar.addStretch()

        board_layout.addLayout(top_bar)

        # Título
        title = QLabel("Niveles")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 30, QFont.Weight.Bold))
        title.setStyleSheet("color: #d4d2d2;")

        board_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop)

        # Grid de niveles
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(20)
        self.grid.setHorizontalSpacing(20)

        self.create_level_grid()
        board_layout.addLayout(self.grid)

        board.setLayout(board_layout)
        main_layout.addWidget(board)
        self.setLayout(main_layout)
       
        from ui.animations.grid_animation import animate_grid_items
        timer = QTimer(self)  # ← self como parent, findChildren lo encuentra
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: animate_grid_items(self.grid))
        timer.start(0)


    def create_level_grid(self):

        # Limpiar grid
        for i in reversed(range(self.grid.count())):
            
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        niveles = self.get_niveles()

        row = 0
        col = 0

        for nivel in niveles:
            
            button = self.create_level_button(nivel)

            self.grid.addWidget(button, row, col,alignment=Qt.AlignmentFlag.AlignCenter)

            col += 1
            if col == 5:
                col = 0
                row += 1
            
    def get_niveles(self):
        return (
        self.session.query(NivelProgreso)
        .order_by(NivelProgreso.nivel)
        .all()
                )

    def create_level_button(self, nivel):

        progreso = (
            self.session.query(NivelProgreso)
            .filter_by(nivel=nivel.nivel)
            .first()
        )

        button = LevelButtonWidget(
            nivel,
            progreso
        )

        button.clicked.connect(
            lambda p=progreso:
            self.open_level(nivel.nivel)
        )

        return button


    def go_back(self):
        self.main_window.navigate_to(self.main_window.home_screen)

    def open_level(self, nivel):
        self.main_window.open_module_screen(nivel)

  