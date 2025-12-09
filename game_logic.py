"""
Модуль игровой логики для игры 'Кто хочет стать миллионером'
"""

import json
import random


class Question:
    """Класс для представления вопроса"""

    def __init__(self, question_id, level, text, options, correct, difficulty):
        self.id = question_id
        self.level = level
        self.text = text
        self.options = options
        self.correct = correct
        self.difficulty = difficulty

    def is_correct(self, answer_index):
        """Проверка правильности ответа"""
        return answer_index == self.correct


class GameState:
    """Класс для управления состоянием игры"""

    def __init__(self, questions_file='questions.json'):
        self.questions_file = questions_file
        self.questions = []
        self.prize_ladder = []
        self.current_level = 0
        self.current_question = None
        self.safe_haven_amounts = []

        # Подсказки
        self.hint_5050_used = False
        self.hint_call_used = False
        self.hint_audience_used = False

        self.load_questions()

    def load_questions(self):
        """Загрузка вопросов из JSON файла"""
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for q_data in data['questions']:
                question = Question(
                    q_data['id'],
                    q_data['level'],
                    q_data['text'],
                    q_data['options'],
                    q_data['correct'],
                    q_data['difficulty']
                )
                self.questions.append(question)

            self.prize_ladder = data['prize_ladder']

            self.safe_haven_amounts = [
                prize['amount'] for prize in self.prize_ladder 
                if prize['safe_haven']
            ]

        except FileNotFoundError:
            raise Exception(f"Файл {self.questions_file} не найден!")
        except json.JSONDecodeError:
            raise Exception(f"Ошибка чтения JSON из файла {self.questions_file}!")

    def start_new_game(self):
        """Начать новую игру"""
        self.current_level = 0
        self.hint_5050_used = False
        self.hint_call_used = False
        self.hint_audience_used = False
        self.load_next_question()

    def load_next_question(self):
        """Загрузить следующий вопрос"""
        if self.current_level < len(self.questions):
            self.current_question = self.questions[self.current_level]
            return True
        return False

    def check_answer(self, answer_index):
        """Проверить ответ игрока"""
        if self.current_question:
            return self.current_question.is_correct(answer_index)
        return False

    def advance_level(self):
        """Перейти на следующий уровень"""
        self.current_level += 1
        return self.load_next_question()

    def get_current_prize(self):
        """Получить текущую сумму выигрыша"""
        if self.current_level == 0:
            return 0
        return self.prize_ladder[self.current_level - 1]['amount']

    def get_safe_haven_prize(self):
        """Получить последнюю несгораемую сумму"""
        current_prize = self.get_current_prize()
        safe_prize = 0

        for amount in self.safe_haven_amounts:
            if amount <= current_prize:
                safe_prize = amount

        return safe_prize

    def is_game_won(self):
        """Проверка, выиграна ли игра"""
        return self.current_level >= len(self.questions)

    def use_hint_5050(self):
        """Использовать подсказку 50/50"""
        if self.hint_5050_used or not self.current_question:
            return None

        self.hint_5050_used = True
        correct_index = self.current_question.correct
        wrong_indices = [i for i in range(4) if i != correct_index]
        keep_wrong = random.choice(wrong_indices)
        remaining = sorted([correct_index, keep_wrong])
        return remaining

    def use_hint_call_friend(self):
        """Использовать подсказку 'Звонок другу'"""
        if self.hint_call_used or not self.current_question:
            return None

        self.hint_call_used = True

        if random.random() < 0.8:
            return self.current_question.correct
        else:
            wrong_indices = [i for i in range(4) if i != self.current_question.correct]
            return random.choice(wrong_indices)

    def use_hint_audience(self):
        """Использовать подсказку 'Помощь зала'"""
        if self.hint_audience_used or not self.current_question:
            return None

        self.hint_audience_used = True
        correct_index = self.current_question.correct
        percentages = {}

        correct_percent = random.randint(40, 60)
        percentages[correct_index] = correct_percent

        remaining = 100 - correct_percent
        wrong_indices = [i for i in range(4) if i != correct_index]

        for i, idx in enumerate(wrong_indices):
            if i == len(wrong_indices) - 1:
                percentages[idx] = remaining
            else:
                percent = random.randint(5, remaining - (len(wrong_indices) - i - 1) * 5)
                percentages[idx] = percent
                remaining -= percent

        return percentages
