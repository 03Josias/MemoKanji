from PyQt6.QtCore import (
    QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup,
    QParallelAnimationGroup, pyqtProperty, QObject, QRect
)
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtGui import QTransform


# ──────────────────────────────────────────────────────────────────────────────
# Helper: objeto intermediario para animar el "scaleX" del widget via geometría
# ──────────────────────────────────────────────────────────────────────────────
class _WidthAnimator(QObject):
    """
    Anima el ancho del widget colapsándolo hacia el centro,
    simulando un flip horizontal (como dar vuelta una tarjeta).
    """

    def __init__(self, widget, base_rect: QRect):
        super().__init__(widget)
        self._widget = widget
        self._base_rect = base_rect  # geometría final / original

    # scaleX va de 0.0 a 1.0
    def _get_scale(self) -> float:
        if self._base_rect.width() == 0:
            return 1.0
        current_w = self._widget.geometry().width()
        return current_w / self._base_rect.width()

    def _set_scale(self, value: float):
        bx = self._base_rect.x()
        bw = self._base_rect.width()
        bh = self._base_rect.height()
        by = self._base_rect.y()

        new_w = max(1, int(bw * value))
        # Centramos el widget mientras se achica/agranda
        new_x = bx + (bw - new_w) // 2
        self._widget.setGeometry(new_x, by, new_w, bh)

    scaleX = pyqtProperty(float, _get_scale, _set_scale)


# ──────────────────────────────────────────────────────────────────────────────
# Función principal
# ──────────────────────────────────────────────────────────────────────────────
def fade_scale_widget(widget, new_text=None, duration=220):
    # Desactivar hover al inicio
    widget.setProperty("animating", True)
    widget._hover_blocked = True

    # ── Efecto de opacidad ──────────────────────────────────────────────────
    opacity = widget.graphicsEffect()
    if not isinstance(opacity, QGraphicsOpacityEffect):
        opacity = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity)
    opacity.setOpacity(1.0)

    # Geometría base (la guardamos ANTES de tocar nada)
    base_rect = widget.geometry()

    # Animador de scaleX
    animator = _WidthAnimator(widget, base_rect)

    # ── FASE 1: EXIT ────────────────────────────────────────────────────────
    exit_group = QParallelAnimationGroup(widget)

    # Colapsar ancho → 0  (InQuad: aceleración suave hacia el centro)
    anim_collapse = QPropertyAnimation(animator, b"scaleX")
    anim_collapse.setDuration(duration)
    anim_collapse.setStartValue(1.0)
    anim_collapse.setEndValue(0.0)
    anim_collapse.setEasingCurve(QEasingCurve.Type.InQuad)

    # Fade out simultáneo (más corto para que "desvanezca" antes del colapso total)
    anim_fade_out = QPropertyAnimation(opacity, b"opacity")
    anim_fade_out.setDuration(int(duration))
    anim_fade_out.setStartValue(1.0)
    anim_fade_out.setEndValue(0.0)

    exit_group.addAnimation(anim_collapse)
    exit_group.addAnimation(anim_fade_out)

    # ── FASE 2: ENTER ───────────────────────────────────────────────────────
    enter_group = QParallelAnimationGroup(widget)

    # Expandir ancho 0 → 1  con rebote pronunciado (OutBack)
    anim_expand = QPropertyAnimation(animator, b"scaleX")
    anim_expand.setDuration(duration + 180)
    anim_expand.setStartValue(0.0)
    anim_expand.setEndValue(1.0)
    bounce = QEasingCurve(QEasingCurve.Type.OutBack)
    bounce.setOvershoot(3.5)          # Rebote visible pero controlado
    anim_expand.setEasingCurve(bounce)

    # Fade in
    anim_fade_in = QPropertyAnimation(opacity, b"opacity")
    anim_fade_in.setDuration(duration + 80)
    anim_fade_in.setStartValue(0.0)
    anim_fade_in.setEndValue(1.0)

    enter_group.addAnimation(anim_expand)
    enter_group.addAnimation(anim_fade_in)

    # ── Swap de contenido entre fases ───────────────────────────────────────
    def _swap_content():
        if new_text is not None and hasattr(widget, "setText"):
            widget.setText(new_text)
        # Aseguramos que el widget quede en la posición base antes de entrar
        widget.setGeometry(base_rect)
        animator._base_rect = base_rect   # por si cambió el layout
        enter_group.start()

    def _on_enter_finished():
        # Reactivar hover al terminar
        widget._hover_blocked = False
        widget.setProperty("animating", False)
    
    exit_group.finished.connect(_swap_content)
    enter_group.finished.connect(_on_enter_finished)  # ← AGREGAR ESTO

    # ── Referencias fuertes (evitar GC) ────────────────────────────────────
    widget._flip_animator  = animator
    widget._flip_exit_anim = exit_group
    widget._flip_enter_anim = enter_group

    exit_group.start()