from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QGridLayout,    QScrollArea  # ← NUEVO

)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from models.kanji import Kanji
from ui.widgets.back_button import BackButton



class KanjiTable(QWidget):

    def __init__(self, main_window, session, nivel):
        super().__init__()

        self.main_window = main_window
        self.session = session
        self.nivel = nivel

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        board = QWidget()
        board.setObjectName("board")
        board.setMinimumSize(1000, 650)
            #2E6F57
            #244333
        board.setStyleSheet("""
            QWidget#board {
                background-color: #2E6F57;
                border: 10px solid #8B5A2B;
                border-radius: 8px;
            }
        """)

        board_layout = QVBoxLayout()
        board_layout.setContentsMargins(40, 25, 40, 25)
        board_layout.setSpacing(20)

        # Top bar
        top_bar = QHBoxLayout()

        back_button = BackButton()
        back_button.clicked.connect(self.go_back)

        title = QLabel(f"Kanji del Nivel {self.nivel}")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #d4d2d2;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_bar.addWidget(back_button)
        top_bar.addStretch()
        top_bar.addWidget(title)
        top_bar.addStretch()

        board_layout.addLayout(top_bar)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        # Tabla
        grid_container = QWidget()
        grid_container.setStyleSheet("background-color: #2E6F57;")  # ← Agregar esto
        self.grid = QGridLayout(grid_container)
        #self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setContentsMargins(5, 5, 5, 5)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
       # self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  # ← Cambiar AlignCenter


        kanji_list = (
            self.session.query(Kanji)
            .filter_by(nivel=self.nivel)
            .order_by(Kanji.orden_global)
            .all()
        )

        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        row = 0
        col = 0

        for kanji in kanji_list:

            kanji_container = QWidget()
            kanji_layout = QVBoxLayout()
            kanji_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            kanji_layout.setSpacing(2)  # Pequeño espacio entre kanji y significado
            kanji_layout.setContentsMargins(1, 1, 1, 1)

            # Kanji (arriba, grande)
            kanji_label = QLabel(kanji.caracter)
            kanji_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            kanji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            kanji_label.setStyleSheet("color: #d4d2d2;")
            kanji_layout.addWidget(kanji_label)

            # Significado (abajo, pequeño)
            meaning_label = QLabel(kanji.significado)
            meaning_label.setFont(QFont("Arial", 10))
            meaning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            meaning_label.setStyleSheet("color: #d4d2d2;")  # Color diferente para distinguir
            meaning_label.setWordWrap(True)  # Permitir salto de línea si es largo
            kanji_layout.addWidget(meaning_label)

            kanji_container.setLayout(kanji_layout)

            self.grid.addWidget(
                kanji_container,
                row,
                col,
                alignment=Qt.AlignmentFlag.AlignCenter
            )

            col += 1
            if col == 10:
                col = 0
                row += 1


        board_layout.addLayout(self.grid)

        scroll_area.setWidget(grid_container)

        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #2E6F57;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: transparent;
                width: 0px;
                height: 0px;
            }
        """)

        board_layout.addWidget(scroll_area)
        board.setLayout(board_layout)
        main_layout.addWidget(board)


        self.setLayout(main_layout)


    def go_back(self):
        self.main_window.open_module_screen(self.nivel)