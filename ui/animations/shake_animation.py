from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint


def apply_shake(widget, amplitude=10, duration=300):

    original_pos = widget.pos()

    animation = QPropertyAnimation(widget, b"pos", widget)
    animation.setDuration(duration)

    # Secuencia de movimiento (izquierda-derecha)
    animation.setKeyValueAt(0.0, original_pos)
    animation.setKeyValueAt(0.1, original_pos + QPoint(-amplitude, 0))
    animation.setKeyValueAt(0.2, original_pos + QPoint(amplitude, 0))
    animation.setKeyValueAt(0.3, original_pos + QPoint(-amplitude, 0))
    animation.setKeyValueAt(0.4, original_pos + QPoint(amplitude, 0))
    animation.setKeyValueAt(0.5, original_pos + QPoint(-amplitude // 2, 0))
    animation.setKeyValueAt(0.6, original_pos + QPoint(amplitude // 2, 0))
    animation.setKeyValueAt(0.7, original_pos + QPoint(-amplitude // 3, 0))
    animation.setKeyValueAt(0.8, original_pos + QPoint(amplitude // 3, 0))
    animation.setKeyValueAt(1.0, original_pos)

    animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    # Guardar referencia (evitar GC)
    widget._shake_anim = animation

    animation.start()
