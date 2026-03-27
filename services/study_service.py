
from models.kanji import Kanji
from models.progreso import ModuloProgreso


class StudyService:

    def __init__(self, session):
        self.session = session

    def get_module_kanji(self, nivel, modulo):
        """
        Devuelve los kanji de un módulo ordenados correctamente.
        """
        kanji_list = (
            self.session.query(Kanji)
            .filter_by(nivel=nivel, modulo=modulo)
            .order_by(Kanji.orden_en_modulo)
            .all()
        )

        return kanji_list

    def mark_as_seen(self, kanji_id):
        """
        Marca un kanji como visto.
        """
        kanji = self.session.query(Kanji).get(kanji_id)
        if kanji:
            kanji.visto = True
            self.session.commit()

    def is_module_unlocked(self, nivel, modulo):
        modulo_obj = (
            self.session.query(ModuloProgreso)
            .filter_by(nivel=nivel, modulo=modulo)
            .first()
        )

        return modulo_obj.desbloqueado if modulo_obj else False