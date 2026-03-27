
from PyQt6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ui.animations.hover_animation import apply_hover_scale
from ui.sounds.sound_manager import SoundManager



class LevelExamButtonWidget(QPushButton):

    clicked = pyqtSignal()

    def __init__(self, nivel, modulos, progreso):
        super().__init__()

        self.nivel = nivel
        self.modulos = modulos
        self.progreso = progreso
        self.clicked.connect(SoundManager.play_click)

        self.setFixedSize(300, 60)
        
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)  

        # Título
        title= QLabel("Examen de nivel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #d4d2d2;")


        layout.addWidget(title)

        # Si completado mostrar estrellas y puntaje

        if self.progreso and self.progreso.completado:

            stars = QLabel("⭐" * self.progreso.estrellas_examen)
            stars.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stars.setFont(QFont("Arial", 16))
            layout.addWidget(stars)

        self.setLayout(layout)
        apply_hover_scale(self)

        self.update_style()

    def update_style(self):
        if all(m.completado for m in self.modulos):

            self.setStyleSheet("""
                QPushButton {
                    background-color: #27634d ;
                    border-radius: 15px;
                    color: #d4d2d2;
                }
                QPushButton:hover {
                    background-color: #1f4f3e;
                }
                """)

        if not all(m.completado for m in self.modulos):
            self.setEnabled(False)

    def mousePressEvent(self, event):

        if self.progreso and not self.progreso.desbloqueado:
            return

        self.clicked.emit()