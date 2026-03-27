from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QEasingCurve, QPoint, QTimer

def animate_screen_entry(direction, widgets, duration=300, offset=200):
    
    if not widgets:
        return
    
    # Calcular offset real
    real_offset = offset if direction else -offset
    
    # Función interna que ejecuta la animación cuando el layout está listo
    def run_animation():
        # Forzar layout
        parent = widgets[0].parentWidget()
        if parent:
            parent.adjustSize()
        
        anim_group = QParallelAnimationGroup()
        
        for widget in widgets:
            if not widget or not widget.isVisible():
                continue
            
            # Guardar posición final (después de adjustSize)
            final_pos = widget.pos()
            
            # Si la posición es inválida, saltar este widget
            if final_pos.x() == 0 and final_pos.y() == 0 and widget != widgets[0]:
                continue
            
            start_pos = QPoint(final_pos.x() + real_offset, final_pos.y())
            
            # Mover a posición inicial sin animar
            widget.move(start_pos)
            
            # Crear animación
            anim = QPropertyAnimation(widget, b"pos")
            anim.setDuration(duration)
            anim.setStartValue(start_pos)
            anim.setEndValue(final_pos)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            anim_group.addAnimation(anim)
        
        anim_group.start()
        
        # Guardar referencia para evitar que se destruya
        for widget in widgets:
            if widget:
                widget._entry_anim_group = anim_group
    
    # Ejecutar en el próximo ciclo del event loop para asegurar layout correcto
    QTimer.singleShot(0, run_animation)