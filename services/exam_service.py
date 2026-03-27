import random
from models.kanji import Kanji
from models.progreso import ModuloProgreso, NivelProgreso


class ExamService:

    def __init__(self, session):
        self.session = session

        self.questions = []
        self.current_index = 0
        self.errors = 0
        self.correct_answers = 0


# CREAR EXAMEN DE MODULO
    def generate_module_exam(self, nivel, modulo):
        """
        Genera examen con los 10 kanji del módulo.
        """
        kanji_list = (
            self.session.query(Kanji)
            .filter_by(nivel=nivel, modulo=modulo)
            .all()
        )

        # Mezclar aleatoriamente
        random.shuffle(kanji_list)

        self.questions = kanji_list

        self.current_index = 0
        self.correct_answers = 0
        self.errors = 0

        return self.questions

# COMPROBAR SI LA RESPUESTA ES CORRECTA
    def evaluate_module_answer(self, kanji, selected_option):

        if kanji.caracter == selected_option:
            
            self.correct_answers += 1
            result = True
        else:
            self.errors += 1
            result= False
            
        self.current_index += 1
        return result

# COMPORBAR SI EL MODULO SIGUE ACTIVO
    def module_exam_active(self):
        return  self.current_index < len(self.questions) and self.errors < 4

# MODULO APROBADO
    def module_passed(self):
        return self.correct_answers >= 7

# DESBLOQUEAR MODULO
    def complete_module(self, nivel, modulo):
        """
        Marca módulo como completado y desbloquea el siguiente.
        """

        modulo_prog = (
            self.session.query(ModuloProgreso)
            .filter_by(nivel=nivel, modulo=modulo)
            .first()
        )

        if not modulo_prog:
            return

        stars = self.calculate_stars()

        modulo_prog.mejor_puntaje = max(
            modulo_prog.mejor_puntaje,
            self.correct_answers
        )

        modulo_prog.estrellas = max(
            modulo_prog.estrellas,
            stars
        )

        modulo_prog.completado = True

        # Desbloquear siguiente módulo
        siguiente = (
            self.session.query(ModuloProgreso)
            .filter_by(nivel=nivel, modulo=modulo + 1)
            .first()
        )

        if siguiente:
            siguiente.desbloqueado = True

        self.session.commit()

# CALCULAR ESTRELLAS DE MODULO
    def calculate_stars(self):
        if self.correct_answers == 10:
            return 3
        elif self.correct_answers >= 8:
            return 2
        elif self.correct_answers >= 7:
            return 1
        return 0

# CALCULAR ESTRELLAS DE EXAMEN DE NIVEL
    def calculate_level_exam_stars(self):

        if self.correct_answers == 50:
            return 3
        elif self.correct_answers >=48 and self.correct_answers <50 :
            return 2
        elif self.correct_answers >= 45 and self.correct_answers < 48:
            return 1
        return 0

# CALCULAR ESTRELLAS DE EXAMEN DE NIVEL
    def calculate_level_stars(self, nivel):
       
        modules = (
            self.session.query(ModuloProgreso)
            .filter_by(nivel=nivel)
            .all()
       )
        countstars=0

        for m in modules:
            countstars+=m.estrellas 

        if countstars == 30:
            return 3
        elif countstars < 30 and countstars>=25 :
            return 2
        elif countstars < 25 :
            return 1

# ACTUALIZAR ESTRELAS DE NIVEL
    def update_level_stars(self, nivel):
        current = (
        self.session.query(NivelProgreso)
            .filter_by(nivel=nivel)
            .first()
        )
        if current.completado:
            current.estrellas = self.calculate_level_stars(nivel)
        self.session.commit()

# VERIFICAR SI TODOS LOS MODULOS ESTAN COMPLETOS
    def all_modules_completed(self, nivel):
        """
        Devuelve True si los 10 módulos del nivel están completados.
        """

        modules = (
            self.session.query(ModuloProgreso)
            .filter_by(nivel=nivel)
            .all()
        )
        if  all(m.completado for m in modules):
            return True
        else:
            return False

# DESBLOQUEA EL SIGUIENTE NIVEL
    def complete_level(self, nivel):
        """
        Marca nivel como completado y desbloquea el siguiente.
        """
        
        #Cargando current level 
        current = (
            self.session.query(NivelProgreso)
            .filter_by(nivel=nivel)
            .first()
        )
        #Compureba si hay current level
        if current:
            print("MARCANDO NIVEL COMPLETADO")
            current.completado = True

        stars = self.calculate_level_exam_stars()

        if current.completado:
            level_stars=self.calculate_level_stars(nivel)
            current.estrellas = max(
            current.estrellas,
            level_stars
            )

        current.mejor_puntaje = max(
            current.mejor_puntaje,
            self.correct_answers
        )

        current.estrellas_examen = max(
            current.estrellas_examen,
            stars
        )

        #Trae el siguiente nivel
        next_level = (
            self.session.query(NivelProgreso)
            .filter_by(nivel=nivel + 1)
            .first()
        )
        #Si hay siguiente nivel lo desbloquea
        if next_level:
            print("DESBLOQUEANDO SIGUIENTE NIVEL")
            next_level.desbloqueado = True

            # Desbloquear módulo 1 del siguiente nivel
            next_module = (
                self.session.query(ModuloProgreso)
                .filter_by(nivel=nivel + 1, modulo=1)
                .first()
            )

            if next_module:
                next_module.desbloqueado = True

        self.session.commit()


# CREAR EXAMEN DE NIVEL
    def generate_level_exam(self, nivel):

        kanji_nivel = (
            self.session.query(Kanji)
            .filter_by(nivel=nivel)
            .all()
        )

        if len(kanji_nivel) < 50:
            raise ValueError("No hay suficientes kanji en el nivel.")

        self.questions = random.sample(kanji_nivel, 50)

        self.current_index = 0
        self.errors = 0
        self.correct_answers = 0

        
        return self.questions

# COMPROBAR SI LA RESPUESTA ES CORRECTA
    def evaluate_level_answer(self, kanji, selected_caracter):

        if kanji.caracter == selected_caracter:
            self.correct_answers += 1
            result = True
        else:
            self.errors += 1
            result= False
        
        self.current_index+=1
        return result

# EXAMEN ACTIVO
    def level_exam_active(self):
        return self.errors < 5 and self.current_index < len(self.questions)

# APROBAR EL EXAMEN
    def level_passed(self):
        return self.correct_answers >= 45
