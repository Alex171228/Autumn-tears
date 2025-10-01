from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QCheckBox, QVBoxLayout, QWidget, QLabel, \
    QComboBox, \
    QPushButton, QDialog, QRadioButton, QFormLayout, QGroupBox, QHBoxLayout, QGridLayout, QLineEdit, QMessageBox, \
    QFileDialog, QFrame, QTextEdit, QDesktopWidget
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5 import QtCore, QtGui
import sys
import os
import lxml
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import requests
import pygame
from copy import deepcopy
from random import choice, randrange, randint
import time
from datetime import datetime
from bs4 import BeautifulSoup as bs

class HoroscopeWorker(QThread):
    horoscope_signal = pyqtSignal(str)

    def __init__(self, sign):
        super().__init__()
        self.sign = sign

    def run(self):
        if not self.check_internet():
            self.horoscope_signal.emit("Вы не подключены к интернету.")
            return

        try:
            text = self.get_horoscope(self.sign)
        except requests.Timeout:
            text = "Время ожидания ответа от сервера истекло."
        except requests.RequestException as e:
            text = f"Сетевая ошибка: {e}"
        except Exception as e:
            text = f"Ошибка: {e}"
        self.horoscope_signal.emit(text)

    def check_internet(self):
        try:
            requests.get("https://www.google.com", timeout=4)
            return True
        except requests.RequestException:
            return False

    def get_horoscope(self, sign):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        }
        base = "https://horoscopes.rambler.ru/"

        r = requests.get(base, headers=headers, timeout=7)
        r.raise_for_status()
        soup = bs(r.text, "lxml")

        # Ищем ссылки на знаки
        candidates = soup.find_all("a")
        zodiac_links, zodiac_names = [], []

        for a in candidates:
            name = (a.get_text() or "").strip()
            href = a.get("href") or ""
            if name in (
                "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
                "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
            ) and href.startswith("/"):
                zodiac_names.append(name)
                zodiac_links.append("https://horoscopes.rambler.ru" + href)

        if sign not in zodiac_names:
            return "Гороскоп для этого знака не найден."

        sign_link = zodiac_links[zodiac_names.index(sign)]

        r2 = requests.get(sign_link, headers=headers, timeout=7)
        r2.raise_for_status()
        soup2 = bs(r2.text, "lxml")

        # Пытаемся найти текст разными способами
        description = None
        for sel in [
            ("p", {"class": "_5yHoW AjIPq"}),
            ("div", {"data-qa": "article"}),
            ("article", {})
        ]:
            tag, attrs = sel
            node = soup2.find(tag, attrs=attrs) if attrs else soup2.find(tag)
            if node:
                if node.name != "p":
                    p = node.find("p")
                    if p:
                        description = p.get_text(" ", strip=True)
                        break
                description = node.get_text(" ", strip=True)
                break

        if not description:
            p = soup2.find("p")
            if p:
                description = p.get_text(" ", strip=True)

        if not description:
            return "Не удалось получить гороскоп."

        return f"<b>{sign}:</b><br>{description}"

class HoroscopeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # QTextEdit для отображения гороскопа
        self.horoscope_text_edit = QTextEdit()
        self.horoscope_text_edit.setReadOnly(True)
        self.horoscope_text_edit.setFont(QFont("Arial", 12))
        self.horoscope_text_edit.setStyleSheet("""
            background-color: #ffffff;
            border: 3px solid red;;
            border-radius: 15px;
        """)

        # Устанавливаем сообщение
        initial_message = """
            <h2 style='text-align: center; margin-top: 50%;'>
                Выберите свой знак зодиака
            </h2>
        """
        self.horoscope_text_edit.setHtml(initial_message)

        layout.addWidget(self.horoscope_text_edit)

        # Кнопки знаков зодиака
        zodiac_signs = [
            "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
            "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
        ]
        zodiac_icons = [
            "oven.jpg", "bul.jpg", "double.jpg", "rak.jpg", "lion.jpg", "ledy.jpg",
            "clock.jpg", "scorp.jpg", "strel.jpg", "koz.jpg", "water.jpg", "fish.jpg",
        ]

        icons_path = os.path.dirname(__file__)

        buttons_layout = QGridLayout()
        for index, sign in enumerate(zodiac_signs):
            button = QPushButton(sign)
            button.setFixedSize(170, 50)
            button.setFont(QFont("Arial", 16))

            # Полный путь к иконке для текущего знака
            icon_path = os.path.join(icons_path, zodiac_icons[index])
            button.setIcon(QIcon(icon_path))

            # Стиль кнопки
            button.setStyleSheet("""
                        background-color: #ffffff;
                        border: 3px solid blue;
                        border-radius: 5px;
                    """)

            # Подключение кнопки к функции показа гороскопа
            button.clicked.connect(lambda checked, s=sign: self.show_horoscope(s))
            buttons_layout.addWidget(button, index // 2, index % 2)

        # Добавляем сетку кнопок к основному макету
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.setFixedHeight(600)
        self.setFixedWidth(700)
    def show_horoscope(self, sign):
        self.horoscope_worker = HoroscopeWorker(sign)
        self.horoscope_worker.horoscope_signal.connect(self.update_horoscope_text_edit)
        self.horoscope_worker.start()

    def update_horoscope_text_edit(self, text):
        if text == "Вы не подключены к интернету.":
            centered_message = f"""
                <h2 style='text-align: center; margin-top: 50%;'>
                    {text}
                </h2>
            """
            self.horoscope_text_edit.setHtml(centered_message)
        else:
            formatted_text = f"<div style='font-size: 27px;'>{text}</div>"
            self.horoscope_text_edit.setHtml(formatted_text)
        self.setVisible(True)