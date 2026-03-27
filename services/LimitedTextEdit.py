
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import Qt


class LimitedTextEdit(QTextEdit):
    """QTextEdit con límite máximo de caracteres"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_length = 668
    
    def keyPressEvent(self, event):
        # Obtener texto actual
        texto_actual = self.toPlainText()
        
        # Teclas que siempre permitir (navegación, borrar, etc.)
        teclas_permitidas = {
            Qt.Key.Key_Backspace,
            Qt.Key.Key_Delete,
            Qt.Key.Key_Left,
            Qt.Key.Key_Right,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down,
            Qt.Key.Key_Home,
            Qt.Key.Key_End,
            Qt.Key.Key_PageUp,
            Qt.Key.Key_PageDown,
            Qt.Key.Key_Control,  # Para atajos como Ctrl+A, Ctrl+C
            Qt.Key.Key_Shift,
            Qt.Key.Key_Alt,
            Qt.Key.Key_Escape,
        }
        
        # Si es tecla de control, permitir
        if event.key() in teclas_permitidas:
            super().keyPressEvent(event)
            return
        
        # Si hay selección, permitir (reemplazar)
        if self.textCursor().hasSelection():
            super().keyPressEvent(event)
            return
        
        # Verificar límite
        if len(texto_actual) >= self.max_length:
            # Ignorar la tecla, no escribir nada
            event.ignore()
            return
        
        # Permitir escritura normal
        super().keyPressEvent(event)
    
    def insertFromMimeData(self, source):
        """Interceptar pegar (Ctrl+V)"""
        texto = source.text()
        texto_actual = self.toPlainText()
        
        # Calcular cuánto cabe
        espacio_disponible = self.max_length - len(texto_actual)
        
        if espacio_disponible <= 0:
            return  # No cabe nada
        
        # Pegar solo lo que cabe
        texto_cortado = texto[:espacio_disponible]
        super().insertPlainText(texto_cortado)