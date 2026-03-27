import sys
import os
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect
from config.config import set_sound_enabled,get_sound_enabled



def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        # subir hasta la raíz del proyecto desde ui/sounds/
        base_path = os.path.join(base_path, "..", "..")
    return os.path.normpath(os.path.join(base_path, relative_path))

class SoundManager:
    sound_enabled = get_sound_enabled()

    click = None
    correct = None
    wrong = None
    write = None
    star = None

    initialized = False

    @classmethod
    def init(cls):
        if cls.initialized:
            return
        
        cls.click = QSoundEffect()
        cls.correct = QSoundEffect()
        cls.wrong = QSoundEffect()
        cls.write = QSoundEffect()
        cls.star = QSoundEffect()

        cls.click.setSource(QUrl.fromLocalFile(get_asset_path("assets/sounds/click.wav")))
        cls.correct.setSource(QUrl.fromLocalFile(get_asset_path("assets/sounds/correct.wav")))
        cls.wrong.setSource(QUrl.fromLocalFile(get_asset_path("assets/sounds/wrong.wav")))
        cls.write.setSource(QUrl.fromLocalFile(get_asset_path("assets/sounds/write.wav")))
        cls.star.setSource(QUrl.fromLocalFile(get_asset_path("assets/sounds/star.wav")))

        cls.click.setVolume(0.5)
        cls.correct.setVolume(0.6)
        cls.wrong.setVolume(0.6)
        cls.write.setVolume(0.7)
        cls.star.setVolume(0.7)

        cls.initialized = True

    @classmethod
    def toggle_sound(cls):
        cls.sound_enabled = not cls.sound_enabled
        cls.click.play()
        set_sound_enabled(cls.sound_enabled)

    @classmethod
    def stop_all(cls):
        for effect in [cls.click, cls.correct, cls.wrong, cls.write, cls.star]:
            if effect and effect.isPlaying():
                effect.stop()
       
    @classmethod
    def play_click(cls):
        if not cls.sound_enabled:
            return
        if cls.click.isLoaded():
            cls.stop_all()
            cls.click.play()

    @classmethod
    def play_correct(cls):
        if not cls.sound_enabled:
            return
        if cls.correct.isLoaded():
            cls.stop_all()
            cls.correct.play()

    @classmethod
    def play_wrong(cls):
        if not cls.sound_enabled:
            return
        if cls.wrong.isLoaded():
            cls.stop_all()
            cls.wrong.play()

    @classmethod
    def play_write(cls):
        if not cls.sound_enabled:
            return
        if cls.write.isLoaded():
            cls.stop_all()
            cls.write.play()

    @classmethod
    def play_star(cls):
        if not cls.sound_enabled:
            return
        if cls.star.isLoaded():
            cls.stop_all()
            cls.star.play()