from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QTimer


def apply_hover_scale(widget, scale=1.02, duration=120):
    
    # Marcar que aún no tenemos geometría válida
    widget._original_geometry = None

    def ensure_original_geometry():
        """Obtener geometría solo cuando sea válida"""
        if widget._original_geometry is None:
            geom = widget.geometry()
            # Solo guardar si tiene tamaño válido (layout ya aplicado)
            if geom.width() > 0 and geom.height() > 0:
                widget._original_geometry = geom
        return widget._original_geometry

    def enter_event(event):
        if getattr(widget, "_hover_blocked", False):
            return  
        if not widget.isEnabled():
            return
        original = ensure_original_geometry()
        if not original:
            # Si aún no hay geometría, no animar
            return

        w, h = original.width(), original.height()
        new_w = int(w * scale)
        new_h = int(h * scale)

        dx = (new_w - w) // 2
        dy = (new_h - h) // 2

        target = QRect(
            original.x() - dx,
            original.y() - dy,
            new_w,
            new_h
        )

        if hasattr(widget, 'anim') and widget.anim.state() == QPropertyAnimation.State.Running:
            widget.anim.stop()

        widget.anim = QPropertyAnimation(widget, b"geometry")
        widget.anim.setDuration(duration)
        widget.anim.setStartValue(widget.geometry())
        widget.anim.setEndValue(target)
        widget.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        widget.anim.start()

    def leave_event(event):
        if getattr(widget, "_hover_blocked", False):  # ← AGREGAR ESTO
            return
        original = ensure_original_geometry()
        if not original:
            return

        if hasattr(widget, 'anim') and widget.anim.state() == QPropertyAnimation.State.Running:
            widget.anim.stop()

        widget.anim = QPropertyAnimation(widget, b"geometry")
        widget.anim.setDuration(duration)
        widget.anim.setStartValue(widget.geometry())
        widget.anim.setEndValue(original)
        widget.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        widget.anim.start()

    widget.enterEvent = enter_event
    widget.leaveEvent = leave_event