from http import server
from math import e
import sys
from PyQt6.QtWidgets import QApplication
import models
from ui.main_window import MainWindow
from ui.screens import study_module_screen
from ui.sounds.sound_manager import SoundManager
from ui.widgets import back_button, level_button, radical_introduction
#pyinstaller --onefile --windowed --ocon=icon.png --name "MemoKanji" main.py 
def main():

    app = QApplication(sys.argv)

    SoundManager.init()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

   
if __name__ == "__main__":
    main()


#kanji_label, exam_level_result_screen, exam_result_screen,explanation_screen (se muestra la primera vez que se abre la aplicación), home_screen, level_exam_sreen, module_exam_screen, moduel_screen, practice_result_screen, practice_screen, study_module_screen, study_screen, module_options, practice_aviso, radical_introduction
# /MemoKanji
#     main.py
#     config.json
#     icon.ico
#     icon.png
#     iniciar_base.py
#     jason_kanji.py
#     jason_radicales.py
#     kanjis.jason
#     modulo3.py
#     pruebas.py
#     raicales.json
#     radicales.py
#     rmd.jason
#     Text.File1.txt
#     assets/
#         sounds/
#             click.wav
#             correct.wav
#             star.wav
#             write.wav
#             wrong.wav
#     config/
#         config.py
#     database/
#         db.py
#         init.py   
#         MemoKanji.db
#     models/
#         kanij.py
#         progreso.py
#         radical.py
#     services/
#         exam_service.py
#         LimitedTextEdit.py
#         practice_service.py
#         study_service.py
#     ui/
#         animations/
#             grid_animation.py
#             hover_aniamtion.py
#             kanji_fade_animation.py
#             shake_animation.py
#             star-animation.py
#             study_switch.py
#         screns/
#             exam_level_result_screen.py
#             exam_result_screen.py
#             home_screen.py
#             module_exam_screen.py
#             module_screen.py
#             practice_result_screen.py
#             practice_screen.py
#             study_module_screen.py
#             study_screen.py
#             tutorial_screen.py
#         sounds/
#             sound_manager.py
#         widgets/
#             back_button.py
#             kanji_table.py
#             level_button.py
#             level_exam_button.py
#             module_button.py 
#             module_option.py 
#             practice_aviso.py 
#             radical_introduction.py 
#         main_window.py
#     venv/