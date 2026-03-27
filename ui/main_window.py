from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt,QPropertyAnimation, QTimer

from database.db import SessionLocal

from services.study_service import StudyService
from services.exam_service import ExamService
from services.practice_service import PracticeService

from ui.screens.study_screen import StudyScreen
from ui.screens.home_screen import HomeScreen
from ui.screens.module_screen import ModuleScreen

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MemoKanji")
        self.setMinimumSize(1000, 700)

        # Base de datos
        self.session = SessionLocal()

        # Servicios
        self.study_service = StudyService(self.session)
        self.exam_service = ExamService(self.session)
        self.practice_service = PracticeService(self.session)

        # Stack de pantallas
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pantalla inicial
        self.home_screen = HomeScreen(self)
        self.stack.addWidget(self.home_screen)
        
        # self.study_screen=StudyScreen(self)
        # self.stack.addWidget(self.study_screen)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        from config.config import load_config
        config=load_config()
        if config["tutorial_visto"]== False:
            self.open_tutorial_screen()
        else:
            self.open_home_screen()

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E6D5B8;  /* Color pared suave */

            }
        """)
    def open_home_screen(self):
        self.home_screen = HomeScreen(self)
        self.stack.addWidget(self.home_screen)
        self.stack.setCurrentWidget(self.home_screen)

    def open_tutorial_screen(self):
        from ui.screens.tutorial_screen import TutorialScreen
        tutorial = TutorialScreen(self)
        self.stack.addWidget(tutorial)
        self.stack.setCurrentWidget(tutorial)

    def finish_tutorial(self):
        from config.config import set_tutorial
        set_tutorial(True)
        self.open_home_screen()

    def navigate_to(self, widget):
        self.stack.setCurrentWidget(widget)
    
    def change_screen(self, new_screen, keep_current=False):

        current = self.stack.currentWidget()

        if current is not None and not keep_current:
           # Cancelar timers pendientes
            for timer in current.findChildren(QTimer):
                timer.stop()
            # Cancelar animaciones activas
            for anim in current.findChildren(QPropertyAnimation):
                anim.stop()
            self.stack.removeWidget(current)
            current.deleteLater()

        self.stack.addWidget(new_screen)
        self.stack.setCurrentWidget(new_screen)

    def open_module_screen(self, nivel):
        module_screen = ModuleScreen(self, nivel)
        
        self.change_screen(module_screen)
