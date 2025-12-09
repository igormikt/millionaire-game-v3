@echo off
echo ================================================
echo Установка библиотек для Millionaire Game
echo Python версия: 3.11.9
echo ================================================
echo.

python --version
echo.

echo Обновление pip...
python -m pip install --upgrade pip

echo.
echo Установка PyInstaller для создания .exe...
pip install pyinstaller==6.3.0

echo.
echo ================================================
echo Установка завершена!
echo ================================================
pause
