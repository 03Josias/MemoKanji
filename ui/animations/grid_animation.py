from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect


def animate_grid_items(layout):
    delay = 0
    parent_widget = layout.parentWidget()  # ← para asignar parent al timer

    for i in range(layout.count()):

        item = layout.itemAt(i).widget()
        if not item:
            continue
        # Limpiar efectos previos
        old_effect = item.graphicsEffect()
        if old_effect:
            item.setGraphicsEffect(None)
        item.parentWidget().adjustSize()
        
        original_pos = item.pos()
        
        if original_pos.x() == 0 and original_pos.y() == 0:
            continue

        # Opacidad inicial
        opacity = QGraphicsOpacityEffect(item)
        opacity.setOpacity(0)
        item.setGraphicsEffect(opacity)
        item.move(original_pos.x(), original_pos.y() + 30)

        # Guardar posición original
        original_pos = item.pos()

        # Mover un poco hacia abajo
        item.move(original_pos.x(), original_pos.y() + 30)

        def start_animation(widget=item, effect=opacity, pos=original_pos):

            widget._hover_blocked = True  # ← BLOQUEAR
            widget._original_geometry = None
            
            fade = QPropertyAnimation(effect, b"opacity")
            fade.setDuration(350)
            fade.setStartValue(0)
            fade.setEndValue(1)
            fade.setEasingCurve(QEasingCurve.Type.OutCubic)

            slide = QPropertyAnimation(widget, b"pos")
            slide.setDuration(350)
            slide.setStartValue(widget.pos())
            slide.setEndValue(pos)
            slide.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            def on_finished():
                widget._hover_blocked = False   # ← DESBLOQUEAR
                widget._original_geometry = None

            slide.finished.connect(on_finished)

            fade.start()
            slide.start()

            widget._fade = fade
            widget._slide = slide

        #QTimer.singleShot(delay, start_animation)
        # ← QTimer con parent en lugar de singleShot estático
        timer = QTimer(parent_widget)
        timer.setSingleShot(True)
        timer.timeout.connect(start_animation)
        timer.start(delay)

        delay += 60

