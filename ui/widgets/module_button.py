from PyQt6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from ui.animations.hover_animation import apply_hover_scale
from ui.sounds.sound_manager import SoundManager

class ModuleButtonWidget(QPushButton):

    clicked = pyqtSignal()

    def __init__(self, nivel, modulo, progreso):
        super().__init__()

        self.nivel = nivel
        self.modulo = modulo
        self.progreso = progreso
        self.clicked.connect(SoundManager.play_click)

        self.setFixedSize(160, 100)
        
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)  

        # Título
        title = QLabel(f"Módulo {self.modulo.modulo}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #d4d2d2;")


        layout.addWidget(title)

        # Si completado mostrar estrellas y puntaje
        if self.progreso and self.progreso.completado:

            stars = QLabel("⭐" * self.progreso.estrellas)
            stars.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stars.setFont(QFont("Arial", 16))
            layout.addWidget(stars)
        
        self.setLayout(layout)

        apply_hover_scale(self)
        self.update_style()

    def update_style(self):

        if self.modulo.desbloqueado:
            color = "#27634d"
        else:
            color = "#4A6B5A"

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 15px;
                color: #d4d2d2;
            }}
            QPushButton:hover {{
                background-color: #1f4f3e;
            }}
        """)
        if not self.modulo.desbloqueado:
            self.setEnabled(False)

    def mousePressEvent(self, event):

        if self.progreso and not self.progreso.desbloqueado:
            return

        self.clicked.emit()