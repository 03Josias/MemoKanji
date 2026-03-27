import random
from datetime import datetime
from re import A
import re
from models.kanji import Kanji
from models.progreso import PracticaProgreso


class PracticeService:

    def __init__(self, session):
        self.session = session
        self.errors = 0
        self.current_streak = 0
        self.progreso = (
            self.session.query(PracticaProgreso)
            .order_by(PracticaProgreso.record_maximo.desc())
            .first()
        )
        self.max_streak=self.progreso.record_maximo
        self.session_counts = {}  # Controla cuántas veces apareció un kanji

    def get_available_kanji(self):
        return (
            self.session.query(Kanji)
            .filter_by(visto=True)
            .all()
        )
    def check_open(self):
        if len(self.get_available_kanji()) < 10:
            return False
        else:
            return True
        
    def get_due_kanji(self):

        now = datetime.utcnow()

        kanji_list = self.get_available_kanji()

        due = []

        for k in kanji_list:
            elapsed = (now - k.ultima_vez).total_seconds() / 86400

            if elapsed >= k.intervalo:
                due.append(k)

        return due
    def get_weighted_random_kanji(self):
        due_kanji = self.get_due_kanji()
        # Elegir fuente: SRS o práctica libre
        if due_kanji:
            source = due_kanji
            weighted = False

        else:
            source = self.get_available_kanji()
            weighted = True  

        if not source:
            return None

        #Limitar repeticiones por sesión
        filtered = [
            k for k in source
            if self.session_counts.get(k.id, 0) < 4
        ]

        if not filtered:
            return None

        #Evitar repetición inmediata
        last_id = getattr(self, "last_kanji_id", None)

        no_repeat = [
            k for k in filtered
            if k.id != last_id
        ]

        if no_repeat:
            filtered = no_repeat  # solo si hay alternativas

        if weighted:
        # Menor facilidad = mayor peso = aparece más seguido
            pesos = [1 / k.facilidad for k in filtered]
            selected = random.choices(filtered, weights=pesos, k=1)[0]
        else:
            selected = random.choice(filtered)
        #Selección final

        #Registrar uso
        self.session_counts[selected.id] = self.session_counts.get(selected.id, 0) + 1
        self.last_kanji_id = selected.id

        return selected

    def evaluate_answer(self, kanji, selected_caracter):
        if kanji.caracter == selected_caracter:

            self.current_streak += 1
            self.max_streak = max(self.max_streak,self.current_streak)
            self._update_weight(kanji, True)
            return True

        else:

            self.errors += 1
            self._update_weight(kanji, False)
            return False

    def _update_weight(self, kanji, correct):
        from datetime import datetime

        now = datetime.utcnow()

        if correct:
            kanji.repeticiones += 1

            if kanji.repeticiones == 1:
                kanji.intervalo = 1
            elif kanji.repeticiones == 2:
                kanji.intervalo = 2
            else:
                kanji.intervalo = min(30,kanji.intervalo * kanji.facilidad +1)

            kanji.facilidad = min(2.5, kanji.facilidad + 0.1)

        else:
            kanji.repeticiones = 0
            kanji.intervalo = 0.5
            kanji.facilidad = max(1.3, kanji.facilidad - 0.2)

        kanji.ultima_vez = now

        self.session.commit()

    def practice_active(self):
        return self.errors < 3

    def reset_practice(self):
         self.errors = 0
         self.current_streak = 0
         self.session_counts = {}

    