"""
Главный файл запуска игры "Кто хочет стать миллионером"
"""

from modern_ui_interface import MillionaireModernUI


def main():
    """Точка входа в приложение"""
    try:
        app = MillionaireModernUI()
        app.run()
    except KeyboardInterrupt:
        print("\nИгра прервана пользователем")
    except Exception as e:
        print("Произошла ошибка: {}".format(e))
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
