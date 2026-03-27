from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from ui.sounds.sound_manager import SoundManager


def animate_stars(star_widgets, delay_step=500):

    delay = 0

    for star in star_widgets:

        # Opacidad inicial
        opacity = QGraphicsOpacityEffect(star)
        star.setGraphicsEffect(opacity)
        opacity.setOpacity(0)

        # Escala inicial simulada con tamaño
        original_size = star.size()
        star.resize(
            int(original_size.width() * 0.4),
            int(original_size.height() * 0.4)
        )

        def start_animation(widget=star, effect=opacity, size=original_size):
            try:
                effect.opacity()  # ← defensa contra destrucción
            except RuntimeError:
                return
            # FADE IN
            fade = QPropertyAnimation(effect, b"opacity")
            fade.setDuration(500)
            fade.setStartValue(0)
            fade.setEndValue(1)
            fade.setEasingCurve(QEasingCurve.Type.OutCubic)

            # SCALE POP
            scale = QPropertyAnimation(widget, b"size")
            scale.setDuration(500)
            scale.setStartValue(widget.size())
            scale.setEndValue(size)
            scale.setEasingCurve(QEasingCurve.Type.OutBack)

            fade.start()
            scale.start()

            widget._fade_anim = fade
            widget._scale_anim = scale
            SoundManager.play_star()

        #QTimer.singleShot(delay, start_animation)
        timer = QTimer(star)
        timer.setSingleShot(True)
        timer.timeout.connect(start_animation)
        timer.start(delay)
        delay += delay_step
