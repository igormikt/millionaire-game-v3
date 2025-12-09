"""
Современный графический интерфейс для игры 'Кто хочет стать миллионером'
Дизайн: Glassmorphism + градиенты + анимации
"""

import tkinter as tk
from tkinter import messagebox
from game_logic import GameState


class ModernButton(tk.Canvas):
    """Современная кнопка с hover-эффектом и анимацией"""

    def __init__(self, parent, text, command, width=200, height=50,
                 bg_color="#667eea", hover_color="#764ba2", **kwargs):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, **kwargs)

        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        self.width = width
        self.height = height
        self.is_hovered = False

        self.draw_button()

        self.text_id = self.create_text(
            width / 2, height / 2,
            text=text,
            font=("Segoe UI", 12, "bold"),
            fill="white"
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def draw_button(self):
        """Рисуем кнопку с градиентом"""
        self.delete("button_bg")

        radius = 15
        color = self.hover_color if self.is_hovered else self.bg_color

        shadow_offset = 3 if not self.is_hovered else 1

        x1 = shadow_offset
        y1 = shadow_offset
        x2 = self.width
        y2 = self.height
        self.create_rounded_rect(x1, y1, x2, y2, radius,
                                 fill="#000000", stipple="gray25",
                                 outline="", tags="button_bg")

        x1 = 0
        y1 = 0
        x2 = self.width - shadow_offset
        y2 = self.height - shadow_offset
        self.create_rounded_rect(x1, y1, x2, y2, radius,
                                 fill=color, outline="", tags="button_bg")

        x1 = 5
        y1 = 5
        x2 = self.width - shadow_offset - 5
        y2 = self.height / 2
        self.create_rounded_rect(x1, y1, x2, y2, radius,
                                 fill="#ffffff", stipple="gray25",
                                 outline="", tags="button_bg")

        self.tag_lower("button_bg")

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Создание скругленного прямоугольника"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        """Эффект при наведении"""
        self.is_hovered = True
        self.draw_button()
        self.config(cursor="hand2")

    def on_leave(self, event):
        """Эффект при уходе курсора"""
        self.is_hovered = False
        self.draw_button()
        self.config(cursor="")

    def on_click(self, event):
        """Обработка клика"""
        if self.command:
            self.command()


class GlassCard(tk.Canvas):
    """Карточка с эффектом стекла (glassmorphism)"""

    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, **kwargs)

        self.width = width
        self.height = height
        self.draw_glass()

    def draw_glass(self):
        """Рисуем стеклянный эффект"""
        radius = 20

        self.create_rounded_rect(
            0, 0, self.width, self.height, radius,
            fill="#1a1a2e", outline="#ffffff", width=1
        )

        self.create_rounded_rect(
            10, 10, self.width - 10, self.height / 3, radius,
            fill="#ffffff", stipple="gray12", outline=""
        )

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Создание скругленного прямоугольника"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class MillionaireModernUI:
    """Главный класс с современным интерфейсом"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Millionaire Game")
        self.root.geometry("1200x750")
        self.root.resizable(False, False)

        self.setup_gradient_background()

        self.game = GameState()
        self.answer_buttons = []
        self.prize_labels = []

        self.show_main_menu()

    def setup_gradient_background(self):
        """Создание градиентного фона"""
        self.bg_canvas = tk.Canvas(self.root, width=1200, height=750,
                                   highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)

        colors = [
            "#667eea", "#6b7ce8", "#707ae6", "#7578e4",
            "#7a76e2", "#7f74e0", "#8472de", "#8970dc",
            "#8e6eda", "#936cd8", "#986ad6", "#9d68d4"
        ]

        height_step = 750 / len(colors)
        for i, color in enumerate(colors):
            y1 = i * height_step
            y2 = (i + 1) * height_step
            self.bg_canvas.create_rectangle(0, y1, 1200, y2,
                                            fill=color, outline="")

        self.bg_canvas.create_oval(-100, -100, 300, 300,
                                   fill="#ffffff", stipple="gray12", outline="")
        self.bg_canvas.create_oval(900, 500, 1400, 900,
                                   fill="#000000", stipple="gray12", outline="")

    def show_main_menu(self):
        """Главное меню"""
        self.clear_window()
        self.setup_gradient_background()

        menu_frame = tk.Frame(self.root, bg="#667eea")
        menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        glass_card = GlassCard(menu_frame, 500, 480, bg="#667eea")
        glass_card.pack()

        title_label = tk.Label(
            glass_card,
            text="MILLIONAIRE\nGAME",
            font=("Segoe UI", 44, "bold"),
            bg="#1a1a2e",
            fg="white"
        )
        glass_card.create_window(250, 110, window=title_label)

        subtitle = tk.Label(
            glass_card,
            text="Кто хочет стать миллионером?",
            font=("Segoe UI", 14),
            bg="#1a1a2e",
            fg="#cccccc"
        )
        glass_card.create_window(250, 190, window=subtitle)

        play_btn = ModernButton(
            glass_card,
            text="НАЧАТЬ ИГРУ",
            command=self.start_game,
            width=280,
            height=60,
            bg_color="#667eea",
            hover_color="#764ba2",
            bg="#1a1a2e"
        )
        glass_card.create_window(250, 290, window=play_btn)

        exit_btn = ModernButton(
            glass_card,
            text="ВЫХОД",
            command=self.root.quit,
            width=280,
            height=60,
            bg_color="#f093fb",
            hover_color="#f5576c",
            bg="#1a1a2e"
        )
        glass_card.create_window(250, 380, window=exit_btn)

    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            if widget != self.bg_canvas:
                widget.destroy()

    def start_game(self):
        """Начать игру"""
        self.game.start_new_game()
        self.show_game_screen()

    def show_game_screen(self):
        """Игровой экран"""
        self.clear_window()
        self.setup_gradient_background()

        main_frame = tk.Frame(self.root, bg="#667eea")
        main_frame.place(x=50, y=50, width=1100, height=650)

        left_frame = tk.Frame(main_frame, bg="#667eea")
        left_frame.place(x=0, y=0, width=750, height=650)

        right_frame = tk.Frame(main_frame, bg="#667eea")
        right_frame.place(x=770, y=0, width=330, height=650)

        hints_card = GlassCard(left_frame, 730, 80, bg="#667eea")
        hints_card.place(x=10, y=0)

        self.hint_5050_btn = self.create_hint_button(
            hints_card, "50:50", 80, 40, "#FF6B6B"
        )
        hints_card.create_window(100, 40, window=self.hint_5050_btn)

        self.hint_call_btn = self.create_hint_button(
            hints_card, "ЗВОНОК", 180, 40, "#4ECDC4"
        )
        hints_card.create_window(300, 40, window=self.hint_call_btn)

        self.hint_audience_btn = self.create_hint_button(
            hints_card, "ЗАЛ", 180, 40, "#95E1D3"
        )
        hints_card.create_window(500, 40, window=self.hint_audience_btn)

        question_card = GlassCard(left_frame, 730, 200, bg="#667eea")
        question_card.place(x=10, y=100)

        self.question_label = tk.Label(
            question_card,
            text="",
            font=("Segoe UI", 18, "bold"),
            bg="#1a1a2e",
            fg="white",
            wraplength=680,
            justify=tk.CENTER
        )
        question_card.create_window(365, 100, window=self.question_label)

        answers_frame = tk.Frame(left_frame, bg="#667eea")
        answers_frame.place(x=10, y=320, width=730, height=320)

        self.answer_buttons = []
        labels = ["A", "B", "C", "D"]

        for i in range(4):
            row = i // 2
            col = i % 2

            btn_frame = tk.Frame(answers_frame, bg="#667eea")
            btn_frame.grid(row=row, column=col, padx=10, pady=10)

            btn = self.create_answer_button(btn_frame, labels[i], i)
            btn.pack()
            self.answer_buttons.append(btn)

        self.create_modern_prize_ladder(right_frame)
        self.display_question()

    def create_hint_button(self, parent, text, width, height, color):
        """Создание кнопки подсказки"""
        btn = ModernButton(
            parent,
            text=text,
            command=lambda t=text: self.use_hint(t),
            width=width,
            height=height,
            bg_color=color,
            hover_color=self.darken_color(color),
            bg="#1a1a2e"
        )
        return btn

    def darken_color(self, hex_color, factor=0.7):
        """Затемнить цвет"""
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def create_answer_button(self, parent, label, index):
        """Создание кнопки ответа"""
        btn = ModernButton(
            parent,
            text="",
            command=lambda: self.select_answer(index),
            width=345,
            height=70,
            bg_color="#3a3a5a",
            hover_color="#4a4a6a",
            bg="#667eea"
        )
        btn.label_text = label
        return btn

    def create_modern_prize_ladder(self, parent):
        """Призовая лестница"""
        prize_card = GlassCard(parent, 310, 630, bg="#667eea")
        prize_card.place(x=10, y=10)

        title = tk.Label(
            prize_card,
            text="ПРИЗЫ",
            font=("Segoe UI", 18, "bold"),
            bg="#1a1a2e",
            fg="#FFD700"
        )
        prize_card.create_window(155, 30, window=title)

        self.prize_labels = []
        reversed_ladder = list(reversed(self.game.prize_ladder))

        y_start = 70
        for i, prize in enumerate(reversed_ladder):
            level = prize['level']
            amount = prize['amount']
            is_safe = prize['safe_haven']

            amount_text = "{:,}".format(amount).replace(",", " ")
            text = "{}.  {} руб".format(level, amount_text)

            if is_safe:
                color = "#FFD700"
                bg_color = "#3a3a2a"
            else:
                color = "white"
                bg_color = "#2a2a3a"

            label = tk.Label(
                prize_card,
                text=text,
                font=("Segoe UI", 11, "bold" if is_safe else "normal"),
                bg=bg_color,
                fg=color,
                width=28,
                height=1,
                relief=tk.FLAT
            )

            prize_card.create_window(155, y_start + i * 38, window=label)
            self.prize_labels.append((level, label))

    def display_question(self):
        """Отобразить вопрос"""
        if not self.game.current_question:
            return

        question = self.game.current_question
        self.question_label.config(text=question.text)

        for i, btn in enumerate(self.answer_buttons):
            btn.bg_color = "#3a3a5a"
            btn.hover_color = "#4a4a6a"

            option_text = "{}: {}".format(btn.label_text, question.options[i])
            btn.text = option_text
            btn.itemconfig(btn.text_id, text=option_text)

            btn.is_hovered = False
            btn.draw_button()

        for i, btn in enumerate(self.answer_buttons):
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
            btn.unbind("<Button-1>")

            btn.bind("<Enter>", btn.on_enter)
            btn.bind("<Leave>", btn.on_leave)
            btn.command = lambda idx=i: self.select_answer(idx)
            btn.bind("<Button-1>", lambda e, b=btn: b.command())

        self.highlight_current_prize()

        if self.game.hint_5050_used:
            self.hint_5050_btn.config(state=tk.DISABLED)
        if self.game.hint_call_used:
            self.hint_call_btn.config(state=tk.DISABLED)
        if self.game.hint_audience_used:
            self.hint_audience_btn.config(state=tk.DISABLED)

    def highlight_current_prize(self):
        """Подсветка приза"""
        current_level = self.game.current_level + 1

        for level, label in self.prize_labels:
            if level == current_level:
                label.config(bg="#667eea", fg="white",
                             font=("Segoe UI", 12, "bold"))
            elif level < current_level:
                label.config(bg="#4CAF50", fg="white")
            else:
                is_safe = any(
                    p['level'] == level and p['safe_haven']
                    for p in self.game.prize_ladder
                )
                if is_safe:
                    label.config(bg="#3a3a2a", fg="#FFD700",
                                 font=("Segoe UI", 11, "bold"))
                else:
                    label.config(bg="#2a2a3a", fg="white",
                                 font=("Segoe UI", 11, "normal"))

    def select_answer(self, answer_index):
        """Выбор ответа"""
        for btn in self.answer_buttons:
            btn.unbind("<Button-1>")
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")

        selected_btn = self.answer_buttons[answer_index]
        selected_btn.bg_color = "#FFA500"
        selected_btn.draw_button()
        self.root.update()
        self.root.after(800)

        if self.game.check_answer(answer_index):
            selected_btn.bg_color = "#4CAF50"
            selected_btn.draw_button()
            self.root.update()
            self.root.after(1000)

            if self.game.advance_level():
                if self.game.is_game_won():
                    self.show_victory()
                else:
                    self.show_correct_dialog()
            else:
                self.show_victory()
        else:
            selected_btn.bg_color = "#f44336"
            selected_btn.draw_button()

            correct_btn = self.answer_buttons[self.game.current_question.correct]
            correct_btn.bg_color = "#4CAF50"
            correct_btn.draw_button()

            self.root.update()
            self.root.after(1500)
            self.show_game_over()

    def show_custom_dialog(self, title, message, icon_color="#4CAF50"):
        """Маленький компактный диалог внизу слева между ответами"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)

        width, height = 320, 170
        dialog.geometry(f"{width}x{height}")
        dialog.configure(bg="#667eea")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Позиция: сильно влево и как можно ниже
        dialog.update_idletasks()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()

        x = root_x + (root_w - width) // 2 - 180  # ещё левее
        y = root_y + root_h - height - 5  # низ окна

        dialog.geometry(f"+{x}+{y}")

        # Стеклянная карточка
        card = GlassCard(dialog, width - 8, height - 8, bg="#667eea")
        card.place(x=4, y=4)

        # Иконка
        icon_canvas = tk.Canvas(card, width=36, height=36,
                                bg="#1a1a2e", highlightthickness=0)
        icon_canvas.place(x=(width - 8) // 2 - 18, y=4)
        icon_canvas.create_oval(3, 3, 33, 33, fill=icon_color, outline="")
        icon_canvas.create_text(18, 18, text="✓",
                                font=("Segoe UI", 16, "bold"), fill="white")

        # Заголовок (чуть выше)
        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg="#1a1a2e",
            fg="white"
        )
        card.create_window((width - 8) // 2, 52, window=title_label)

        # Сообщение ближе к заголовку (меньше расстояние между строками)
        msg_label = tk.Label(
            card,
            text=message,
            font=("Segoe UI", 9),
            bg="#1a1a2e",
            fg="#dddddd",
            justify=tk.CENTER
        )
        card.create_window((width - 8) // 2, 86, window=msg_label)

        dialog.result = None

        def on_yes():
            dialog.result = True
            dialog.destroy()

        def on_no():
            dialog.result = False
            dialog.destroy()

        btn_frame = tk.Frame(card, bg="#1a1a2e")
        card.create_window((width - 8) // 2, height - 40, window=btn_frame)

        yes_btn = ModernButton(
            btn_frame,
            text="ДА",
            command=on_yes,
            width=70,
            height=30,
            bg_color="#4CAF50",
            hover_color="#45a049",
            bg="#1a1a2e"
        )
        yes_btn.pack(side=tk.LEFT, padx=4)

        no_btn = ModernButton(
            btn_frame,
            text="НЕТ",
            command=on_no,
            width=70,
            height=30,
            bg_color="#f44336",
            hover_color="#da190b",
            bg="#1a1a2e"
        )
        no_btn.pack(side=tk.LEFT, padx=4)

        dialog.wait_window()
        return dialog.result

    def show_correct_dialog(self):
        """Диалог правильного ответа"""
        prize = self.game.get_current_prize()
        prize_text = "{:,}".format(prize).replace(",", " ")

        message = "Правильный ответ!   Ваш выигрыш: {} руб\nПродолжить игру?".format(prize_text)
        result = self.show_custom_dialog("Отлично! ✨", message, "#4CAF50")

        if result:
            self.display_question()
        else:
            self.show_take_money()

    def show_game_over(self):
        """Окно проигрыша"""
        safe_prize = self.game.get_safe_haven_prize()
        prize_text = "{:,}".format(safe_prize).replace(",", " ")

        message = "Неправильный ответ   Вы выиграли: {} руб\nСыграть еще раз?".format(prize_text)
        result = self.show_custom_dialog("Игра окончена", message, "#FF9800")

        if result:
            self.start_game()
        else:
            self.show_main_menu()

    def show_victory(self):
        """Окно победы"""
        max_prize = self.game.prize_ladder[-1]['amount']
        prize_text = "{:,}".format(max_prize).replace(",", " ")

        message = "НЕВЕРОЯТНО!\n\nВЫ ВЫИГРАЛИ {} руб!\n\nСыграть еще раз?".format(prize_text)
        result = self.show_custom_dialog("ПОЗДРАВЛЯЕМ! 🎉", message, "#FFD700")

        if result:
            self.start_game()
        else:
            self.show_main_menu()

    def show_take_money(self):
        """Забрать деньги"""
        prize = self.game.get_current_prize()
        prize_text = "{:,}".format(prize).replace(",", " ")

        message = "Вы забираете деньги!\n\nВаш выигрыш: {} руб\n\nСыграть еще раз?".format(prize_text)
        result = self.show_custom_dialog("Поздравляем! 💰", message, "#4CAF50")

        if result:
            self.start_game()
        else:
            self.show_main_menu()

    def use_hint(self, hint_type):
        """Использование подсказок"""
        if "50:50" in hint_type:
            self.use_hint_5050()
        elif "ЗВОНОК" in hint_type:
            self.use_hint_call()
        elif "ЗАЛ" in hint_type:
            self.use_hint_audience()

    def use_hint_5050(self):
        """Подсказка 50/50"""
        remaining = self.game.use_hint_5050()

        if remaining:
            self.hint_5050_btn.config(state=tk.DISABLED)

            for i in range(4):
                if i not in remaining:
                    btn = self.answer_buttons[i]
                    btn.bg_color = "#1a1a1a"
                    btn.draw_button()
                    btn.unbind("<Button-1>")
                    btn.unbind("<Enter>")
                    btn.unbind("<Leave>")

    def use_hint_call(self):
        """Звонок другу"""
        answer_index = self.game.use_hint_call_friend()

        if answer_index is not None:
            self.hint_call_btn.config(state=tk.DISABLED)

            labels = ["A", "B", "C", "D"]
            messagebox.showinfo(
                "Звонок другу",
                "Друг думает: {}\n\n{}".format(
                    labels[answer_index],
                    self.game.current_question.options[answer_index]
                )
            )

    def use_hint_audience(self):
        """Помощь зала"""
        percentages = self.game.use_hint_audience()

        if percentages:
            self.hint_audience_btn.config(state=tk.DISABLED)
            self.show_audience_window(percentages)

    def show_audience_window(self, percentages):
        """Окно помощи зала"""
        window = tk.Toplevel(self.root)
        window.title("Помощь зала")
        window.geometry("500x400")
        window.configure(bg="#667eea")
        window.transient(self.root)
        window.grab_set()

        title = tk.Label(
            window,
            text="Результаты голосования зала",
            font=("Segoe UI", 16, "bold"),
            bg="#667eea",
            fg="white"
        )
        title.pack(pady=20)

        chart_frame = tk.Frame(window, bg="#667eea")
        chart_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)

        labels = ["A", "B", "C", "D"]
        colors = ["#FF6B6B", "#4ECDC4", "#95E1D3", "#FFD93D"]

        sorted_percentages = sorted(percentages.items())

        for i, (idx, percent) in enumerate(sorted_percentages):
            frame = tk.Frame(chart_frame, bg="#667eea")
            frame.pack(pady=8, fill=tk.X)

            label = tk.Label(
                frame,
                text="{}:".format(labels[idx]),
                font=("Segoe UI", 14, "bold"),
                bg="#667eea",
                fg="white",
                width=3
            )
            label.pack(side=tk.LEFT)

            bar_canvas = tk.Canvas(
                frame,
                width=300,
                height=35,
                bg="#3a3a5a",
                highlightthickness=0
            )
            bar_canvas.pack(side=tk.LEFT, padx=10)

            fill_width = int(300 * percent / 100)
            bar_canvas.create_rectangle(
                0, 0, fill_width, 35,
                fill=colors[i],
                outline=""
            )

            percent_label = tk.Label(
                frame,
                text="{}%".format(percent),
                font=("Segoe UI", 14, "bold"),
                bg="#667eea",
                fg="white"
            )
            percent_label.pack(side=tk.LEFT)

        close_btn = ModernButton(
            window,
            text="ЗАКРЫТЬ",
            command=window.destroy,
            width=200,
            height=50,
            bg_color="#f093fb",
            hover_color="#f5576c",
            bg="#667eea"
        )
        close_btn.pack(pady=20)

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()
