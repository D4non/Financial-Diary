import sys
import json
from PyQt5 import QtWidgets, QtGui, QtCore

# Основное окно
class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QVBoxLayout()

        ### НАСТРОЙКА ВКЛАДОК
        self.tabs = QtWidgets.QTabWidget() #Создаём объект для вкладок
        # Создаём все вкладки
        self.tab_main = QtWidgets.QWidget()
        self.tab_income = QtWidgets.QWidget()
        self.tab_expenditure = QtWidgets.QWidget()
        self.tab_history = QtWidgets.QWidget()
        self.tab_settings = QtWidgets.QWidget()

        # Именуем вкладки
        self.tabs.addTab(self.tab_main, "Главная")
        self.tabs.addTab(self.tab_income, "Доходы")
        self.tabs.addTab(self.tab_expenditure, "Расходы")
        self.tabs.addTab(self.tab_history, "История")
        self.tabs.addTab(self.tab_settings, "Настройки")


        ### ГЛАВНАЯ СТРАНИЦА
        self.vbox_main = QtWidgets.QVBoxLayout()
        self.hbox_main = QtWidgets.QHBoxLayout()

        self.background_main = QtWidgets.QGroupBox() # Слой для круглой обводки суммы
        self.background_main.setStyleSheet("border: 2px solid rgba(0,0,0,50); border-radius: 10px;")
        self.background_main.setFixedHeight(100)
        self.background_main2 = QtWidgets.QVBoxLayout()

        # Название
        self.title_main = QtWidgets.QLabel('Финансовый дневник')
        self.title_main.setStyleSheet("font: 20pt")
        self.title_main.setAlignment(QtCore.Qt.AlignCenter)

        # Подсчитываем имеющиеся деньги с учётом доходов и расходов
        self.amount = 0
        with open('history.json', 'r', encoding='utf-8') as f:  # Открыли файл json
            text = json.load(f)  # Всё содержимое файла переписали в переменную

        for txt in text['history']: # Пробежались по данным
            money = txt['total'] # Все значение total записали в переменную money
            type = txt['type'] # Аналогично с типом операции (доход или расход)

            # В зависимости от типа операции добавляем или вычитаем деньги из общей суммы
            if type == 'income':
                self.amount += money
            else:
                self.amount -= money

        # Общая сумма
        self.total_main = QtWidgets.QLabel(str(self.amount) + ' ₽')
        self.total_main.setStyleSheet("border: 0; border-radius: 0px; font: 14pt")
        self.total_main.setAlignment(QtCore.Qt.AlignCenter)

        # Кнопка для добавления дохода
        self.btn_addIncome_main = QtWidgets.QPushButton('(+) Доход')
        self.btn_addIncome_main.setFixedSize(150, 75)
        self.btn_addIncome_main.setStyleSheet("font: 12pt")
        self.btn_addIncome_main.clicked.connect(self.addIncomeFunc)

        # Кнопка для добавления расхода
        self.btn_addExpenditure_main = QtWidgets.QPushButton('(-) Расход')
        self.btn_addExpenditure_main.setFixedSize(150, 75)
        self.btn_addExpenditure_main.setStyleSheet("font: 12pt")
        self.btn_addExpenditure_main.clicked.connect(self.addExpenditureFunc)

        # Кнопка для перехода на вкладку истории
        self.btn_history_main = QtWidgets.QPushButton('История')
        self.btn_history_main.setFixedSize(150, 75)
        self.btn_history_main.setStyleSheet("font: 12pt")
        self.btn_history_main.clicked.connect(self.openHistory)

        # Кнопка для перехода на вкладку настроек
        self.btn_settings_main = QtWidgets.QPushButton('Настройки')
        self.btn_settings_main.setFixedSize(150, 75)
        self.btn_settings_main.setStyleSheet("font: 12pt")
        self.btn_settings_main.clicked.connect(self.openSettings)

        # Добавляем все кнопки и заголовки на слой
        self.hbox_main.addWidget(self.btn_addIncome_main)
        self.hbox_main.addWidget(self.btn_addExpenditure_main)
        self.hbox_main.addWidget(self.btn_history_main)
        self.hbox_main.addWidget(self.btn_settings_main)

        # Добавляем слой на фон самого приложения
        self.background_main2.addWidget(self.total_main)
        self.background_main.setLayout(self.background_main2)

        self.vbox_main.addWidget(self.title_main)
        self.vbox_main.addWidget(self.background_main)
        self.vbox_main.addLayout(self.hbox_main)

        # Добавляем всё на вкладку основную вкладку
        self.tab_main.setLayout(self.vbox_main)


        ### СТРАНИЦА ДОХОДОВ
        self.vbox_income = QtWidgets.QVBoxLayout()
        self.hbox_income = QtWidgets.QHBoxLayout()

        # Создаём заголовок и прописываем ему стиль
        self.title_income = QtWidgets.QLabel('Доходы:')
        self.title_income.setStyleSheet("font: 28pt")
        self.title_income.setAlignment(QtCore.Qt.AlignCenter)

        # Рассчитываем все доходы аналогично как на основной вкладке
        self.amount_income = 0
        # Только в этот раз пробегаемся по файлу json где хранятся все доходы
        with open('income.json', 'r', encoding='utf-8') as f:
            text = json.load(f)

        for txt in text['income']:
            money = txt['total']
            self.amount_income += money

        # Создаём текстовый заголовок с общей суммой доходов
        self.total_income = QtWidgets.QLabel('+ ' + str(self.amount_income) + ' ₽')
        self.total_income.setStyleSheet("font: 20pt")
        self.total_income.setAlignment(QtCore.Qt.AlignCenter)

        # Создаём кнопку для добавления новых доходов
        self.btn_add_income = QtWidgets.QPushButton('Добавить')
        self.btn_add_income.setFixedSize(200, 70)
        self.btn_add_income.setStyleSheet("font: 14pt")
        self.btn_add_income.clicked.connect(self.addIncomeFunc)

        # Помещаем всё на общий слой
        self.hbox_income.addWidget(self.btn_add_income)

        self.vbox_income.addWidget(self.title_income)
        self.vbox_income.addWidget(self.total_income)
        self.vbox_income.addLayout(self.hbox_income)

        # Делаем этот слой основным для вкладки с доходами
        self.tab_income.setLayout(self.vbox_income)


        ### СТРАНИЦА РАСХОДОВ
        self.vbox_expenditure = QtWidgets.QVBoxLayout()
        self.hbox_expenditure = QtWidgets.QHBoxLayout()

        # Создаём заголовок и прописываем ему стиль
        self.title_expenditure = QtWidgets.QLabel('Расходы:')
        self.title_expenditure.setStyleSheet("font: 28pt")
        self.title_expenditure.setAlignment(QtCore.Qt.AlignCenter)

        # Рассчитываем все расходы аналогично как на основной вкладке
        self.amount_expenditure = 0
        # Только в этот раз пробегаемся по файлу json где хранятся все расходы
        with open('expenditure.json', 'r', encoding='utf-8') as f:
            text = json.load(f)

        for txt in text['expenditure']:
            money = txt['total']
            self.amount_expenditure += money

        # Создаём текстовый заголовок с общей суммой расходов
        self.total_expenditure = QtWidgets.QLabel('- ' + str(self.amount_expenditure) + ' ₽')
        self.total_expenditure.setStyleSheet("font: 20pt")
        self.total_expenditure.setAlignment(QtCore.Qt.AlignCenter)

        # Создаём кнопку для добавления новых расходов
        self.btn_add_expenditure = QtWidgets.QPushButton('Добавить')
        self.btn_add_expenditure.setFixedSize(200, 70)
        self.btn_add_expenditure.setStyleSheet("font: 14pt")
        self.btn_add_expenditure.clicked.connect(self.addExpenditureFunc)

        # Помещаем всё на общий слой
        self.hbox_expenditure.addWidget(self.btn_add_expenditure)

        self.vbox_expenditure.addWidget(self.title_expenditure)
        self.vbox_expenditure.addWidget(self.total_expenditure)
        self.vbox_expenditure.addLayout(self.hbox_expenditure)

        # Делаем этот слой основным для вкладки с расходами
        self.tab_expenditure.setLayout(self.vbox_expenditure)



        ### СТРАНИЦА ИСТОРИИ
        self.vbox_history = QtWidgets.QVBoxLayout()
        self.layout_history = QtWidgets.QGridLayout()
        self.hbox_history = QtWidgets.QHBoxLayout()

        # Создаём отдельный объект для того чтобы историю можно было скроллить (листать)
        self.scroll = QtWidgets.QScrollArea()

        # Пробегаемся по всему файлу с историей и записываем данные в перемнную
        with open('history.json', 'r', encoding='utf-8') as f:
            text = json.load(f)

        # Считываем и записываем в соответствующие переменные дату, сумму, описание и тип для каждой операции
        for txt in text['history']:
            self.date = txt['date']
            self.total = txt['total']
            self.description = txt['description']
            self.type = txt['type']

            # Создам специальный объект, который будет отдельной ячейкой для каждой операции в скролле
            # В оглавлении будет дата, когда была выполнена операция
            self.cell = QtWidgets.QGroupBox(self.date)

            # В зависимости от типа операции прописываем + или - в каждой ячейке и сумму операции
            self.total_lbl = QtWidgets.QLabel()
            if self.type == 'income':
                self.total_lbl.setText('+ ' + str(self.total))
            else:
                self.total_lbl.setText('- ' + str(self.total))

            # Создаём объект для описания операции
            self.desc_lbl = QtWidgets.QLabel(self.description)

            # Добавляем все объекты на слои и добавляем ячейку в скролл
            self.vbox_story = QtWidgets.QVBoxLayout()
            self.vbox_story.addWidget(self.total_lbl)
            self.vbox_story.addWidget(self.desc_lbl)

            self.cell.setLayout(self.vbox_story)
            self.layout_history.addWidget(self.cell)

        self.widget_history = QtWidgets.QWidget()
        self.widget_history.setLayout(self.layout_history)

        self.scroll.setWidget(self.widget_history)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)

        # Создаём заголовок
        self.title_history = QtWidgets.QLabel('История:')
        self.title_history.setStyleSheet("font: 20pt")
        self.title_history.setAlignment(QtCore.Qt.AlignCenter)

        # Создам кнпоки добавить доход
        self.btn_addIncome_history = QtWidgets.QPushButton('(+) Доход')
        self.btn_addIncome_history.setFixedSize(150, 60)
        self.btn_addIncome_history.setStyleSheet("font: 12pt")
        self.btn_addIncome_history.clicked.connect(self.addIncomeFunc)

        # Добавить расход
        self.btn_addExpenditure_history = QtWidgets.QPushButton('(-) Расход')
        self.btn_addExpenditure_history.setFixedSize(150, 60)
        self.btn_addExpenditure_history.setStyleSheet("font: 12pt")
        self.btn_addExpenditure_history.clicked.connect(self.addExpenditureFunc)

        # Удалить последнюю операцию
        self.btn_delete_history = QtWidgets.QPushButton('Удалить')
        self.btn_delete_history.setFixedSize(150, 60)
        self.btn_delete_history.setStyleSheet("font: 12pt")
        self.btn_delete_history.clicked.connect(self.deleteHistory)

        # Добавляем всё на слой, а слой на вкладку
        self.hbox_history.addWidget(self.btn_addIncome_history)
        self.hbox_history.addWidget(self.btn_addExpenditure_history)
        self.hbox_history.addWidget(self.btn_delete_history)

        self.vbox_history.addWidget(self.title_history)
        self.vbox_history.addWidget(self.scroll)
        self.vbox_history.addLayout(self.hbox_history)

        self.tab_history.setLayout(self.vbox_history)



        ### СТРАНИЦА НАСТРОЕК
        self.vbox_settings = QtWidgets.QVBoxLayout()
        self.hbox_settings = QtWidgets.QHBoxLayout()

        # Создаём заголовок
        self.title_settings = QtWidgets.QLabel('Настройки')
        self.title_settings.setStyleSheet("font: 28pt")
        self.title_settings.setAlignment(QtCore.Qt.AlignCenter)

        # Заголовок предществующий выбору языка
        self.language = QtWidgets.QLabel('Язык:')
        self.language.setStyleSheet("font: 20pt")

        # Объект для выбора языка
        self.setLanguage = QtWidgets.QComboBox()
        self.setLanguage.addItem('Русский')
        self.setLanguage.addItem('English')
        self.setLanguage.setFixedHeight(75)
        self.setLanguage.setStyleSheet("font: 13pt")

        # Кнопку сохранить которая будет считывать изменения
        self.btn_save_settings = QtWidgets.QPushButton('Cохранить')
        self.btn_save_settings.setFixedSize(150, 60)
        self.btn_save_settings.setStyleSheet("font: 12pt")
        self.btn_save_settings.clicked.connect(self.save_settings)

        # Добавляем всё на слои и на вкладку
        self.hbox_settings.addWidget(self.btn_save_settings)

        self.vbox_settings.addWidget(self.title_settings)
        self.vbox_settings.addWidget(self.language)
        self.vbox_settings.addWidget(self.setLanguage)
        self.vbox_settings.addLayout(self.hbox_settings)

        self.tab_settings.setLayout(self.vbox_settings)




        # Добавляем вкладки в приложение
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        # Прописываем название окну нашего приложения
        self.setWindowTitle('Дневник финансов')


    # Функция показывающая окно для добавления дохода
    def addIncomeFunc(self):
        ai.show()

    # Функция показывающая окно для добавления дохода
    def addExpenditureFunc(self):
        ae.show()

    # Функция считывающая изменения языка, и взависмости от выбора, показывающая нужное окно
    def save_settings(self):
        language = self.setLanguage.currentText()

        if language == 'Русский':
            mw.show()
        else:
            mw.close()
            Emw.show()

    # Функция для открытия вкладки с историей
    def openHistory(self):
        self.tabs.setCurrentIndex(3)

    # Функция для открытия вкладки с историей
    def openSettings(self):
        self.tabs.setCurrentIndex(4)

    # Функция, удаляющая последнюю операцию из истории
    def deleteHistory(self):
        # Смотрим есть ли у нас вообще операции
        if self.layout_history.count() != 0:
            # Если есть:
            with open('history.json', 'r', encoding='utf8') as f: # Пробегаемся по файлу с историей
                data = json.load(f) # Записываем всё в одну переменную
                deduction = data['history'][-1]['total'] # Ищем сумму вычета
                type = data['history'][-1]['type'] # Ищем тип последней операции
                # Если это доход
                if type == 'income':
                    with open('income.json', 'r', encoding='utf8') as fi:
                        data_income = json.load(fi)
                        del data_income['income'][-1] # Удаляем последнюю операцию из файла с доходами
                        with open('income.json', 'w', encoding='utf8') as outfile:
                            json.dump(data_income, outfile, ensure_ascii=False, indent=2) # Переписываем файл по новой без последней операции
                        del data['history'][-1] # Удаляем последнюю операцию из файла с историей
                        with open('history.json', 'w', encoding='utf8') as outfile:
                            json.dump(data, outfile, ensure_ascii=False, indent=2) # Переписываем файл по новой без последней операции
                # Если это расход
                else:
                    with open('expenditure.json', 'r', encoding='utf8') as fi:
                        data_expenditure = json.load(fi)
                        del data_expenditure['expenditure'][-1] # Удаляем последнюю операцию из файла с расходами
                        with open('expenditure.json', 'w', encoding='utf8') as outfile:
                            json.dump(data_expenditure, outfile, ensure_ascii=False, indent=2) # Переписываем файл по новой без последней операции
                        del data['history'][-1] # Удаляем последнюю операцию из файла с историей
                        with open('history.json', 'w', encoding='utf8') as outfile:
                            json.dump(data, outfile, ensure_ascii=False, indent=2) # Переписываем файл по новой без последней операции

            for i in reversed(range(self.layout_history.count())):
                self.layout_history.itemAt(i).widget().setParent(None) # Удаляем последнюю ячейку из скролла
            for i in reversed(range(Emw.layout_history.count())):
                Emw.layout_history.itemAt(i).widget().setParent(None) # Удаляем все ячейки из скролла

            with open('history.json', 'r', encoding='utf-8') as f: # Открываем файл с историей
                text = json.load(f) # Переписываем всё в одну переменную

            # Ищем дату, сумму, описание и тип операции
            for txt in text['history']:
                self.date = txt['date']
                self.total = txt['total']
                self.description = txt['description']
                self.type = txt['type']

                # Переделываем весь скролл по новому по новым данным без последней операции
                self.cell = QtWidgets.QGroupBox(self.date)

                self.total_lbl = QtWidgets.QLabel()
                if self.type == 'income':
                    self.total_lbl.setText('+ ' + str(self.total))
                else:
                    self.total_lbl.setText('- ' + str(self.total))

                self.desc_lbl = QtWidgets.QLabel(self.description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                self.layout_history.addWidget(self.cell)

                # Ищем дату, сумму, описание и тип операции
                for txt in text['history']:
                    self.date = txt['date']
                    self.total = txt['total']
                    self.description = txt['description']
                    self.type = txt['type']

                    # Переделываем весь скролл по новому по новым данным без последней операции
                    self.cell = QtWidgets.QGroupBox(self.date)

                    self.total_lbl = QtWidgets.QLabel()
                    if self.type == 'income':
                        self.total_lbl.setText('+ ' + str(self.total))
                    else:
                        self.total_lbl.setText('- ' + str(self.total))

                    self.desc_lbl = QtWidgets.QLabel(self.description)

                    self.vbox_story = QtWidgets.QVBoxLayout()
                    self.vbox_story.addWidget(self.total_lbl)
                    self.vbox_story.addWidget(self.desc_lbl)

                    self.cell.setLayout(self.vbox_story)
                    Emw.layout_history.addWidget(self.cell)

            # Если тип операции доход, то вычитаем удалённую сумму из общей суммы и суммы доходов
            if type == 'income':
                self.amount -= deduction
                self.total_main.setText(str(mw.amount) + ' ₽')
                Emw.total_main.setText(str(mw.amount) + ' ₽')
                self.amount_income -= deduction
                self.total_income.setText('+ ' + str(mw.amount_income) + ' ₽')
                Emw.total_income.setText('+ ' + str(mw.amount_income) + ' ₽')
            # Если тип операции расход, то вычитаем удалённую сумму из общей суммы и суммы расходов
            else:
                self.amount += deduction
                self.total_main.setText(str(mw.amount) + ' ₽')
                Emw.total_main.setText(str(mw.amount) + ' ₽')
                self.amount_expenditure -= deduction
                self.total_expenditure.setText('- ' + str(mw.amount_expenditure) + ' ₽')
                Emw.total_expenditure.setText('- ' + str(mw.amount_expenditure) + ' ₽')




# Окно для добавления дохода
class AddIncome(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox2 = QtWidgets.QHBoxLayout()

        # Создаём заголовок
        self.title = QtWidgets.QLabel('Добавить доход:')
        self.title.setStyleSheet("font: 18pt")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        # Заголовок предществующий введению суммы
        self.summa = QtWidgets.QLabel('Сумма:')
        self.summa.setStyleSheet("font: 10pt")
        # Поле ввода суммы
        self.editSumma = QtWidgets.QLineEdit()
        self.editSumma.setStyleSheet("font: 9pt")

        # Заголовок предществующий введению описания
        self.description = QtWidgets.QLabel('Описание:')
        self.description.setStyleSheet("font: 10pt")
        # Поле ввода описания
        self.editDescription = QtWidgets.QLineEdit()
        self.editDescription.setStyleSheet("font: 9pt")

        # Кнопка для сохранения операции
        self.save = QtWidgets.QPushButton('Сохранить')
        self.save.clicked.connect(self.addIncome)
        self.save.setFixedSize(150, 40)
        self.save.setStyleSheet("font: 9pt")

        # Кнопка для очистки полей
        self.delete = QtWidgets.QPushButton('Очистить')
        self.delete.clicked.connect(self.clear)
        self.delete.setFixedSize(150, 40)
        self.delete.setStyleSheet("font: 9pt")

        # Кнопка для закрытия окна
        self.btn_close = QtWidgets.QPushButton('Закрыть')
        self.btn_close.clicked.connect(self.closeWindow)
        self.btn_close.setFixedSize(150, 40)
        self.btn_close.setStyleSheet("font: 9pt")

        # Добавляем всё на слои
        self.hbox1.addWidget(self.save)
        self.hbox1.addWidget(self.delete)

        self.hbox2.addWidget(self.btn_close)

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.summa)
        self.vbox.addWidget(self.editSumma)
        self.vbox.addWidget(self.description)
        self.vbox.addWidget(self.editDescription)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.setLayout(self.vbox)
        # Название окна
        self.setWindowTitle('Добавить доход')

    # Функция для очистки полей
    def clear(self):
        self.editSumma.clear()
        self.editDescription.clear()

    # Функция для закрытия окна
    def closeWindow(self):
        self.editSumma.clear()
        self.editDescription.clear()
        ai.close()

    # Функция для добавление дохода
    def addIncome(self):
        # Проверяем на ошибки
        try:
            # Если вс хорошо, оставляем текст обычным
            self.summa.setText('Сумма:')
            self.summa.setStyleSheet("font: 10pt;")

            # С помощью встроенным функций находим сегодняшнюю дату и записываем её
            date = (QtCore.QDate.currentDate()).toString(QtCore.Qt.ISODate)
            # Считываем сумму операции с поля ввода
            summa = float(self.editSumma.text())
            # Считываем описание операции с поля ввода
            description = self.editDescription.text()

            # Если сумма больше нуля
            if summa > 0:
                # Добавляем данные операции в файл с историей и файл с доходами
                new_data = {'date': date, 'total': summa, 'description': description}
                with open('income.json', encoding='utf8') as f:
                    data = json.load(f)
                    data['income'].append(new_data)
                    with open('income.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=2)

                new_data = {'date': date, 'total': summa, 'description': description, 'type': 'income'}
                with open('history.json', encoding='utf8') as f:
                    data = json.load(f)
                    data['history'].append(new_data)
                    with open('history.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=2)

                # Добавляем новую ячейку в скролле истории
                self.cell = QtWidgets.QGroupBox(date)

                self.total_lbl = QtWidgets.QLabel('+ ' + str(summa))
                self.desc_lbl = QtWidgets.QLabel(description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                mw.layout_history.addWidget(self.cell)


                # Добавляем новую ячейку в скролле истории
                self.cell = QtWidgets.QGroupBox(date)

                self.total_lbl = QtWidgets.QLabel('+ ' + str(summa))
                self.desc_lbl = QtWidgets.QLabel(description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                Emw.layout_history.addWidget(self.cell)

                # Вычитаем и добавляем сумму дохода в основной вкладке и вкладке с доходами
                mw.amount += summa
                mw.total_main.setText(str(mw.amount) + ' ₽')
                mw.amount_income += summa
                mw.total_income.setText('+ ' + str(mw.amount_income) + ' ₽')
                Emw.amount += summa
                Emw.total_main.setText(str(mw.amount) + ' ₽')
                Emw.amount_income += summa
                Emw.total_income.setText('+ ' + str(mw.amount_income) + ' ₽')
            # Если сумма меньше нуля, то выводим ошибку и подсвечиваем красным
            else:
                self.summa.setText('Сумма: Число не может быть меньше 0!')
                self.summa.setStyleSheet("font: 10pt; color: red;")
        # Если введены не числовые данные, то выводим ошибку и подсвечиваем красным
        except ValueError:
            self.summa.setText('Сумма: Данные введены неверно!')
            self.summa.setStyleSheet("font: 10pt; color: red;")



# Окно для добавления расхода
class AddExpenditure(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox2 = QtWidgets.QHBoxLayout()

        # Создаём заголовок
        self.title = QtWidgets.QLabel('Добавить расход:')
        self.title.setStyleSheet("font: 18pt")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        # Заголовок предществующий введению суммы
        self.summa = QtWidgets.QLabel('Сумма:')
        self.summa.setStyleSheet("font: 10pt")
        # Поле ввода суммы
        self.editSumma = QtWidgets.QLineEdit()
        self.editSumma.setStyleSheet("font: 9pt")

        # Заголовок предществующий введению описания
        self.description = QtWidgets.QLabel('Описание:')
        self.description.setStyleSheet("font: 10pt")
        # Поле ввода описания
        self.editDescription = QtWidgets.QLineEdit()
        self.editDescription.setStyleSheet("font: 9pt")

        # Кнопка для сохранения операции
        self.save = QtWidgets.QPushButton('Сохранить')
        self.save.clicked.connect(self.addExpenditure)
        self.save.setFixedSize(150, 40)
        self.save.setStyleSheet("font: 9pt")

        # Кнопка для очистки полей
        self.delete = QtWidgets.QPushButton('Очистить')
        self.delete.clicked.connect(self.clear)
        self.delete.setFixedSize(150, 40)
        self.delete.setStyleSheet("font: 9pt")

        # Кнопка для закрытия окна
        self.btn_close = QtWidgets.QPushButton('Закрыть')
        self.btn_close.clicked.connect(self.closeWindow)
        self.btn_close.setFixedSize(150, 40)
        self.btn_close.setStyleSheet("font: 9pt")

        # Добавляем всё на слои
        self.hbox1.addWidget(self.save)
        self.hbox1.addWidget(self.delete)

        self.hbox2.addWidget(self.btn_close)

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.summa)
        self.vbox.addWidget(self.editSumma)
        self.vbox.addWidget(self.description)
        self.vbox.addWidget(self.editDescription)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.setLayout(self.vbox)
        # Название окна
        self.setWindowTitle('Добавить расход')

    # Функция для очистки полей
    def clear(self):
        self.editSumma.clear()
        self.editDescription.clear()

    # Функция для закрытия окна
    def closeWindow(self):
        self.editSumma.clear()
        self.editDescription.clear()
        ae.close()

    # Функция для добавление расхода
    def addExpenditure(self):
        # Проверяем на ошибки
        try:
            # Если вс хорошо, оставляем текст обычным
            self.summa.setText('Сумма:')
            self.summa.setStyleSheet("font: 10pt;")

            # С помощью встроенным функций находим сегодняшнюю дату и записываем её
            date = (QtCore.QDate.currentDate()).toString(QtCore.Qt.ISODate)
            # Считываем сумму операции с поля ввода
            summa = float(self.editSumma.text())
            # Считываем описание операции с поля ввода
            description = self.editDescription.text()

            # Если сумма больше нуля
            if summa > 0:
                # Добавляем данные операции в файл с историей и файл с расходами
                new_data = {'date': date, 'total': summa, 'description': description}
                with open('expenditure.json', encoding='utf8') as f:
                    data = json.load(f)
                    data['expenditure'].append(new_data)
                    with open('expenditure.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=2)

                new_data = {'date': date, 'total': summa, 'description': description, 'type': 'expenditure'}
                with open('history.json', encoding='utf8') as f:
                    data = json.load(f)
                    data['history'].append(new_data)
                    with open('history.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=2)

                # Добавляем новую ячейку в скролле истории
                self.cell = QtWidgets.QGroupBox(date)

                self.total_lbl = QtWidgets.QLabel('- ' + str(summa))
                self.desc_lbl = QtWidgets.QLabel(description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                mw.layout_history.addWidget(self.cell)

                # Добавляем новую ячейку в скролле истории
                self.cell = QtWidgets.QGroupBox(date)

                self.total_lbl = QtWidgets.QLabel('- ' + str(summa))
                self.desc_lbl = QtWidgets.QLabel(description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                Emw.layout_history.addWidget(self.cell)

                # Вычитаем и добавляем сумму расхода в основной вкладке и вкладке с раходами
                mw.amount -= summa
                mw.total_main.setText(str(mw.amount) + ' ₽')
                mw.amount_expenditure += summa
                mw.total_expenditure.setText('- ' + str(mw.amount_expenditure) + ' ₽')
                Emw.amount -= summa
                Emw.total_main.setText(str(mw.amount) + ' ₽')
                Emw.amount_expenditure += summa
                Emw.total_expenditure.setText('- ' + str(mw.amount_expenditure) + ' ₽')
            # Если сумма меньше нуля, то выводим ошибку и подсвечиваем красным
            else:
                self.summa.setText('Сумма: Число не может быть меньше 0!')
                self.summa.setStyleSheet("font: 10pt; color: red;")
        # Если введены не числовые данные, то выводим ошибку и подсвечиваем красным
        except ValueError:
            self.summa.setText('Сумма: Данные введены неверно!')
            self.summa.setStyleSheet("font: 10pt; color: red;")







# Основное окно
class ENMainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QVBoxLayout()

        ### НАСТРОЙКА ВКЛАДОК
        self.tabs = QtWidgets.QTabWidget() #Создаём объект для вкладок
        # Создаём все вкладки
        self.tab_main = QtWidgets.QWidget()
        self.tab_income = QtWidgets.QWidget()
        self.tab_expenditure = QtWidgets.QWidget()
        self.tab_history = QtWidgets.QWidget()
        self.tab_settings = QtWidgets.QWidget()

        # Именуем вкладки
        self.tabs.addTab(self.tab_main, "Main")
        self.tabs.addTab(self.tab_income, "Income")
        self.tabs.addTab(self.tab_expenditure, "Expenses")
        self.tabs.addTab(self.tab_history, "History")
        self.tabs.addTab(self.tab_settings, "Settings")


        ### ГЛАВНАЯ СТРАНИЦА
        self.vbox_main = QtWidgets.QVBoxLayout()
        self.hbox_main = QtWidgets.QHBoxLayout()

        self.background_main = QtWidgets.QGroupBox() # Слой для круглой обводки суммы
        self.background_main.setStyleSheet("border: 2px solid rgba(0,0,0,50); border-radius: 10px;")
        self.background_main.setFixedHeight(100)
        self.background_main2 = QtWidgets.QVBoxLayout()

        # Название
        self.title_main = QtWidgets.QLabel('Financial Diary')
        self.title_main.setStyleSheet("font: 20pt")
        self.title_main.setAlignment(QtCore.Qt.AlignCenter)

        # Подсчитываем имеющиеся деньги с учётом доходов и расходов
        self.amount = 0
        with open('history.json', 'r', encoding='utf-8') as f:  # Открыли файл json
            text = json.load(f)  # Всё содержимое файла переписали в переменную

        for txt in text['history']: # Пробежались по данным
            money = txt['total'] # Все значение total записали в переменную money
            type = txt['type'] # Аналогично с типом операции (доход или расход)

            # В зависимости от типа операции добавляем или вычитаем деньги из общей суммы
            if type == 'income':
                self.amount += money
            else:
                self.amount -= money

        # Общая сумма
        self.total_main = QtWidgets.QLabel(str(self.amount) + ' ₽')
        self.total_main.setStyleSheet("border: 0; border-radius: 0px; font: 14pt")
        self.total_main.setAlignment(QtCore.Qt.AlignCenter)

        # Кнопка для добавления дохода
        self.btn_addIncome_main = QtWidgets.QPushButton('(+) Income')
        self.btn_addIncome_main.setFixedSize(150, 75)
        self.btn_addIncome_main.setStyleSheet("font: 12pt")
        self.btn_addIncome_main.clicked.connect(self.addIncomeFunc)

        # Кнопка для добавления расхода
        self.btn_addExpenditure_main = QtWidgets.QPushButton('(-) Expense')
        self.btn_addExpenditure_main.setFixedSize(150, 75)
        self.btn_addExpenditure_main.setStyleSheet("font: 12pt")
        self.btn_addExpenditure_main.clicked.connect(self.addExpenditureFunc)

        # Кнопка для перехода на вкладку истории
        self.btn_history_main = QtWidgets.QPushButton('History')
        self.btn_history_main.setFixedSize(150, 75)
        self.btn_history_main.setStyleSheet("font: 12pt")
        self.btn_history_main.clicked.connect(self.openHistory)

        # Кнопка для перехода на вкладку настроек
        self.btn_settings_main = QtWidgets.QPushButton('Settings')
        self.btn_settings_main.setFixedSize(150, 75)
        self.btn_settings_main.setStyleSheet("font: 12pt")
        self.btn_settings_main.clicked.connect(self.openSettings)

        # Добавляем все кнопки и заголовки на слой
        self.hbox_main.addWidget(self.btn_addIncome_main)
        self.hbox_main.addWidget(self.btn_addExpenditure_main)
        self.hbox_main.addWidget(self.btn_history_main)
        self.hbox_main.addWidget(self.btn_settings_main)

        # Добавляем слой на фон самого приложения
        self.background_main2.addWidget(self.total_main)
        self.background_main.setLayout(self.background_main2)

        self.vbox_main.addWidget(self.title_main)
        self.vbox_main.addWidget(self.background_main)
        self.vbox_main.addLayout(self.hbox_main)

        # Добавляем всё на вкладку основную вкладку
        self.tab_main.setLayout(self.vbox_main)


        ### СТРАНИЦА ДОХОДОВ
        self.vbox_income = QtWidgets.QVBoxLayout()
        self.hbox_income = QtWidgets.QHBoxLayout()

        # Создаём заголовок и прописываем ему стиль
        self.title_income = QtWidgets.QLabel('Income:')
        self.title_income.setStyleSheet("font: 28pt")
        self.title_income.setAlignment(QtCore.Qt.AlignCenter)

        # Рассчитываем все доходы аналогично как на основной вкладке
        self.amount_income = 0
        # Только в этот раз пробегаемся по файлу json где хранятся все доходы
        with open('income.json', 'r', encoding='utf-8') as f:
            text = json.load(f)

        for txt in text['income']:
            money = txt['total']
            self.amount_income += money

        # Создаём текстовый заголовок с общей суммой доходов
        self.total_income = QtWidgets.QLabel('+ ' + str(self.amount_income) + ' ₽')
        self.total_income.setStyleSheet("font: 20pt")
        self.total_income.setAlignment(QtCore.Qt.AlignCenter)

        # Создаём кнопку для добавления новых доходов
        self.btn_add_income = QtWidgets.QPushButton('Add')
        self.btn_add_income.setFixedSize(200, 70)
        self.btn_add_income.setStyleSheet("font: 14pt")
        self.btn_add_income.clicked.connect(self.addIncomeFunc)

        # Помещаем всё на общий слой
        self.hbox_income.addWidget(self.btn_add_income)

        self.vbox_income.addWidget(self.title_income)
        self.vbox_income.addWidget(self.total_income)
        self.vbox_income.addLayout(self.hbox_income)

        # Делаем этот слой основным для вкладки с доходами
        self.tab_income.setLayout(self.vbox_income)


        ### СТРАНИЦА РАСХОДОВ
        self.vbox_expenditure = QtWidgets.QVBoxLayout()
        self.hbox_expenditure = QtWidgets.QHBoxLayout()

        # Создаём заголовок и прописываем ему стиль
        self.title_expenditure = QtWidgets.QLabel('Expenses:')
        self.title_expenditure.setStyleSheet("font: 28pt")
        self.title_expenditure.setAlignment(QtCore.Qt.AlignCenter)

        # Рассчитываем все расходы аналогично как на основной вкладке
        self.amount_expenditure = 0
        # Только в этот раз пробегаемся по файлу json где хранятся все расходы
        with open('expenditure.json', 'r', encoding='utf-8') as f:
            text = json.load(f)

        for txt in text['expenditure']:
            money = txt['total']
            self.amount_expenditure += money

        # Создаём текстовый заголовок с общей суммой расходов
        self.total_expenditure = QtWidgets.QLabel('- ' + str(self.amount_expenditure) + ' ₽')
        self.total_expenditure.setStyleSheet("font: 20pt")
        self.total_expenditure.setAlignment(QtCore.Qt.AlignCenter)

        # Создаём кнопку для добавления новых расходов
        self.btn_add_expenditure = QtWidgets.QPushButton('Add')
        self.btn_add_expenditure.setFixedSize(200, 70)
        self.btn_add_expenditure.setStyleSheet("font: 14pt")
        self.btn_add_expenditure.clicked.connect(self.addExpenditureFunc)

        # Помещаем всё на общий слой
        self.hbox_expenditure.addWidget(self.btn_add_expenditure)

        self.vbox_expenditure.addWidget(self.title_expenditure)
        self.vbox_expenditure.addWidget(self.total_expenditure)
        self.vbox_expenditure.addLayout(self.hbox_expenditure)

        # Делаем этот слой основным для вкладки с расходами
        self.tab_expenditure.setLayout(self.vbox_expenditure)



        ### СТРАНИЦА ИСТОРИИ
        self.vbox_history = QtWidgets.QVBoxLayout()
        self.layout_history = QtWidgets.QGridLayout()
        self.hbox_history = QtWidgets.QHBoxLayout()

        # Создаём отдельный объект для того чтобы историю можно было скроллить (листать)
        self.scroll = QtWidgets.QScrollArea()

        # Пробегаемся по всему файлу с историей и записываем данные в перемнную
        with open('history.json', 'r', encoding='utf-8') as f:
            text = json.load(f)

        # Считываем и записываем в соответствующие переменные дату, сумму, описание и тип для каждой операции
        for txt in text['history']:
            self.date = txt['date']
            self.total = txt['total']
            self.description = txt['description']
            self.type = txt['type']

            # Создам специальный объект, который будет отдельной ячейкой для каждой операции в скролле
            # В оглавлении будет дата, когда была выполнена операция
            self.cell = QtWidgets.QGroupBox(self.date)

            # В зависимости от типа операции прописываем + или - в каждой ячейке и сумму операции
            self.total_lbl = QtWidgets.QLabel()
            if self.type == 'income':
                self.total_lbl.setText('+ ' + str(self.total))
            else:
                self.total_lbl.setText('- ' + str(self.total))

            # Создаём объект для описания операции
            self.desc_lbl = QtWidgets.QLabel(self.description)

            # Добавляем все объекты на слои и добавляем ячейку в скролл
            self.vbox_story = QtWidgets.QVBoxLayout()
            self.vbox_story.addWidget(self.total_lbl)
            self.vbox_story.addWidget(self.desc_lbl)

            self.cell.setLayout(self.vbox_story)
            self.layout_history.addWidget(self.cell)

        self.widget_history = QtWidgets.QWidget()
        self.widget_history.setLayout(self.layout_history)

        self.scroll.setWidget(self.widget_history)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)

        # Создаём заголовок
        self.title_history = QtWidgets.QLabel('History:')
        self.title_history.setStyleSheet("font: 20pt")
        self.title_history.setAlignment(QtCore.Qt.AlignCenter)

        # Создам кнпоки добавить доход
        self.btn_addIncome_history = QtWidgets.QPushButton('(+) Income')
        self.btn_addIncome_history.setFixedSize(150, 60)
        self.btn_addIncome_history.setStyleSheet("font: 12pt")
        self.btn_addIncome_history.clicked.connect(self.addIncomeFunc)

        # Добавить расход
        self.btn_addExpenditure_history = QtWidgets.QPushButton('(-) Expense')
        self.btn_addExpenditure_history.setFixedSize(150, 60)
        self.btn_addExpenditure_history.setStyleSheet("font: 12pt")
        self.btn_addExpenditure_history.clicked.connect(self.addExpenditureFunc)

        # Удалить последнюю операцию
        self.btn_delete_history = QtWidgets.QPushButton('Delete')
        self.btn_delete_history.setFixedSize(150, 60)
        self.btn_delete_history.setStyleSheet("font: 12pt")
        self.btn_delete_history.clicked.connect(self.deleteHistory)

        # Добавляем всё на слой, а слой на вкладку
        self.hbox_history.addWidget(self.btn_addIncome_history)
        self.hbox_history.addWidget(self.btn_addExpenditure_history)
        self.hbox_history.addWidget(self.btn_delete_history)

        self.vbox_history.addWidget(self.title_history)
        self.vbox_history.addWidget(self.scroll)
        self.vbox_history.addLayout(self.hbox_history)

        self.tab_history.setLayout(self.vbox_history)



        ### СТРАНИЦА НАСТРОЕК
        self.vbox_settings = QtWidgets.QVBoxLayout()
        self.hbox_settings = QtWidgets.QHBoxLayout()

        # Создаём заголовок
        self.title_settings = QtWidgets.QLabel('Settings')
        self.title_settings.setStyleSheet("font: 28pt")
        self.title_settings.setAlignment(QtCore.Qt.AlignCenter)

        # Заголовок предществующий выбору языка
        self.language = QtWidgets.QLabel('Language:')
        self.language.setStyleSheet("font: 20pt")

        # Объект для выбора языка
        self.setLanguage = QtWidgets.QComboBox()
        self.setLanguage.addItem('Русский')
        self.setLanguage.addItem('English')
        self.setLanguage.setFixedHeight(75)
        self.setLanguage.setStyleSheet("font: 13pt")

        # Кнопку сохранить которая будет считывать изменения
        self.btn_save_settings = QtWidgets.QPushButton('Save')
        self.btn_save_settings.setFixedSize(150, 60)
        self.btn_save_settings.setStyleSheet("font: 12pt")
        self.btn_save_settings.clicked.connect(self.save_settings)

        # Добавляем всё на слои и на вкладку
        self.hbox_settings.addWidget(self.btn_save_settings)

        self.vbox_settings.addWidget(self.title_settings)
        self.vbox_settings.addWidget(self.language)
        self.vbox_settings.addWidget(self.setLanguage)
        self.vbox_settings.addLayout(self.hbox_settings)

        self.tab_settings.setLayout(self.vbox_settings)




        # Добавляем вкладки в приложение
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        # Прописываем название окну нашего приложения
        self.setWindowTitle('Financial Diary')


    # Функция показывающая окно для добавления дохода
    def addIncomeFunc(self):
        Eai.show()

    # Функция показывающая окно для добавления дохода
    def addExpenditureFunc(self):
        Eae.show()

    # Функция считывающая изменения языка, и взависмости от выбора, показывающая нужное окно
    def save_settings(self):
        language = self.setLanguage.currentText()

        if language == 'Русский':
            mw.show()
            Emw.close()
        else:
            Emw.show()

    # Функция для открытия вкладки с историей
    def openHistory(self):
        self.tabs.setCurrentIndex(3)

    # Функция для открытия вкладки с историей
    def openSettings(self):
        self.tabs.setCurrentIndex(4)

    # Функция, удаляющая последнюю операцию из истории
    def deleteHistory(self):
        # Смотрим есть ли у нас вообще операции
        if self.layout_history.count() != 0:
            # Если есть:
            with open('history.json', 'r', encoding='utf8') as f: # Пробегаемся по файлу с историей
                data = json.load(f) # Записываем всё в одну переменную
                deduction = data['history'][-1]['total'] # Ищем сумму вычета
                type = data['history'][-1]['type'] # Ищем тип последней операции
                # Если это доход
                if type == 'income':
                    with open('income.json', 'r', encoding='utf8') as fi:
                        data_income = json.load(fi)
                        del data_income['income'][-1] # Удаляем последнюю операцию из файла с доходами
                        with open('income.json', 'w', encoding='utf8') as outfile:
                            json.dump(data_income, outfile, ensure_ascii=False, indent=2) # Переписываем файл по новой без последней операции
                        del data['history'][-1] # Удаляем последнюю операцию из файла с историей
                        with open('history.json', 'w', encoding='utf8') as outfile:
                            json.dump(data, outfile, ensure_ascii=False, indent=2) # Переписываем файл по новой без последней операции
                # Если это расход
                else:
                    with open('expenditure.json', 'r', encoding='utf8') as fi:
                        data_expenditure = json.load(fi)
                        del data_expenditure['expenditure'][-1] # Удаляем последнюю операцию из файла с расходами
                        with open('expenditure.json', 'w', encoding='utf8') as outfile:
                            json.dump(data_expenditure, outfile, ensure_ascii=False, indent=2) # Переписываем файл по новой без последней операции
                        del data['history'][-1] # Удаляем последнюю операцию из файла с историей
                        with open('history.json', 'w', encoding='utf8') as outfile:
                            json.dump(data, outfile, ensure_ascii=False, indent=2) # Переписываем файл по новой без последней операции

            for i in reversed(range(self.layout_history.count())):
                self.layout_history.itemAt(i).widget().setParent(None)  # Удаляем все ячейки из скролла
            for i in reversed(range(mw.layout_history.count())):
                mw.layout_history.itemAt(i).widget().setParent(None) # Удаляем все ячейки из скролла

            with open('history.json', 'r', encoding='utf-8') as f: # Открываем файл с историей
                text = json.load(f) # Переписываем всё в одну переменную

            # Ищем дату, сумму, описание и тип операции
            for txt in text['history']:
                self.date = txt['date']
                self.total = txt['total']
                self.description = txt['description']
                self.type = txt['type']

                # Переделываем весь скролл по новому по новым данным без последней операции
                self.cell = QtWidgets.QGroupBox(self.date)

                self.total_lbl = QtWidgets.QLabel()
                if self.type == 'income':
                    self.total_lbl.setText('+ ' + str(self.total))
                else:
                    self.total_lbl.setText('- ' + str(self.total))

                self.desc_lbl = QtWidgets.QLabel(self.description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                self.layout_history.addWidget(self.cell)

                # Ищем дату, сумму, описание и тип операции
                for txt in text['history']:
                    self.date = txt['date']
                    self.total = txt['total']
                    self.description = txt['description']
                    self.type = txt['type']

                    # Переделываем весь скролл по новому по новым данным без последней операции
                    self.cell = QtWidgets.QGroupBox(self.date)

                    self.total_lbl = QtWidgets.QLabel()
                    if self.type == 'income':
                        self.total_lbl.setText('+ ' + str(self.total))
                    else:
                        self.total_lbl.setText('- ' + str(self.total))

                    self.desc_lbl = QtWidgets.QLabel(self.description)

                    self.vbox_story = QtWidgets.QVBoxLayout()
                    self.vbox_story.addWidget(self.total_lbl)
                    self.vbox_story.addWidget(self.desc_lbl)

                    self.cell.setLayout(self.vbox_story)
                    mw.layout_history.addWidget(self.cell)

            # Если тип операции доход, то вычитаем удалённую сумму из общей суммы и суммы доходов
            if type == 'income':
                self.amount -= deduction
                self.total_main.setText(str(Emw.amount) + ' ₽')
                mw.total_main.setText(str(Emw.amount) + ' ₽')
                self.amount_income -= deduction
                self.total_income.setText('+ ' + str(Emw.amount_income) + ' ₽')
                mw.total_income.setText('+ ' + str(Emw.amount_income) + ' ₽')
            # Если тип операции расход, то вычитаем удалённую сумму из общей суммы и суммы расходов
            else:
                self.amount += deduction
                self.total_main.setText(str(Emw.amount) + ' ₽')
                mw.total_main.setText(str(Emw.amount) + ' ₽')
                self.amount_expenditure -= deduction
                self.total_expenditure.setText('- ' + str(Emw.amount_expenditure) + ' ₽')
                mw.total_expenditure.setText('- ' + str(Emw.amount_expenditure) + ' ₽')




# Окно для добавления дохода
class ENAddIncome(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox2 = QtWidgets.QHBoxLayout()

        # Создаём заголовок
        self.title = QtWidgets.QLabel('Add Income:')
        self.title.setStyleSheet("font: 18pt")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        # Заголовок предществующий введению суммы
        self.summa = QtWidgets.QLabel('Total:')
        self.summa.setStyleSheet("font: 10pt")
        # Поле ввода суммы
        self.editSumma = QtWidgets.QLineEdit()
        self.editSumma.setStyleSheet("font: 9pt")

        # Заголовок предществующий введению описания
        self.description = QtWidgets.QLabel('Description:')
        self.description.setStyleSheet("font: 10pt")
        # Поле ввода описания
        self.editDescription = QtWidgets.QLineEdit()
        self.editDescription.setStyleSheet("font: 9pt")

        # Кнопка для сохранения операции
        self.save = QtWidgets.QPushButton('Save')
        self.save.clicked.connect(self.addIncome)
        self.save.setFixedSize(150, 40)
        self.save.setStyleSheet("font: 9pt")

        # Кнопка для очистки полей
        self.delete = QtWidgets.QPushButton('Clear')
        self.delete.clicked.connect(self.clear)
        self.delete.setFixedSize(150, 40)
        self.delete.setStyleSheet("font: 9pt")

        # Кнопка для закрытия окна
        self.btn_close = QtWidgets.QPushButton('Close')
        self.btn_close.clicked.connect(self.closeWindow)
        self.btn_close.setFixedSize(150, 40)
        self.btn_close.setStyleSheet("font: 9pt")

        # Добавляем всё на слои
        self.hbox1.addWidget(self.save)
        self.hbox1.addWidget(self.delete)

        self.hbox2.addWidget(self.btn_close)

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.summa)
        self.vbox.addWidget(self.editSumma)
        self.vbox.addWidget(self.description)
        self.vbox.addWidget(self.editDescription)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.setLayout(self.vbox)
        # Название окна
        self.setWindowTitle('Add Income')

    # Функция для очистки полей
    def clear(self):
        self.editSumma.clear()
        self.editDescription.clear()

    # Функция для закрытия окна
    def closeWindow(self):
        self.editSumma.clear()
        self.editDescription.clear()
        Eai.close()

    # Функция для добавление дохода
    def addIncome(self):
        # Проверяем на ошибки
        try:
            # Если вс хорошо, оставляем текст обычным
            self.summa.setText('Total:')
            self.summa.setStyleSheet("font: 10pt;")

            # С помощью встроенным функций находим сегодняшнюю дату и записываем её
            date = (QtCore.QDate.currentDate()).toString(QtCore.Qt.ISODate)
            # Считываем сумму операции с поля ввода
            summa = float(self.editSumma.text())
            # Считываем описание операции с поля ввода
            description = self.editDescription.text()

            # Если сумма больше нуля
            if summa > 0:
                # Добавляем данные операции в файл с историей и файл с доходами
                new_data = {'date': date, 'total': summa, 'description': description}
                with open('income.json', encoding='utf8') as f:
                    data = json.load(f)
                    data['income'].append(new_data)
                    with open('income.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=2)

                new_data = {'date': date, 'total': summa, 'description': description, 'type': 'income'}
                with open('history.json', encoding='utf8') as f:
                    data = json.load(f)
                    data['history'].append(new_data)
                    with open('history.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=2)

                # Добавляем новую ячейку в скролле истории
                self.cell = QtWidgets.QGroupBox(date)

                self.total_lbl = QtWidgets.QLabel('+ ' + str(summa))
                self.desc_lbl = QtWidgets.QLabel(description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                Emw.layout_history.addWidget(self.cell)

                # Добавляем новую ячейку в скролле истории
                self.cell = QtWidgets.QGroupBox(date)

                self.total_lbl = QtWidgets.QLabel('+ ' + str(summa))
                self.desc_lbl = QtWidgets.QLabel(description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                mw.layout_history.addWidget(self.cell)

                # Вычитаем и добавляем сумму дохода в основной вкладке и вкладке с доходами
                Emw.amount += summa
                Emw.total_main.setText(str(Emw.amount) + ' ₽')
                Emw.amount_income += summa
                Emw.total_income.setText('+ ' + str(Emw.amount_income) + ' ₽')
                mw.amount += summa
                mw.total_main.setText(str(Emw.amount) + ' ₽')
                mw.amount_income += summa
                mw.total_income.setText('+ ' + str(Emw.amount_income) + ' ₽')
            # Если сумма меньше нуля, то выводим ошибку и подсвечиваем красным
            else:
                self.summa.setText('Total: The number cannot be less than 0!')
                self.summa.setStyleSheet("font: 10pt; color: red;")
        # Если введены не числовые данные, то выводим ошибку и подсвечиваем красным
        except ValueError:
            self.summa.setText('Total: The data is entered incorrectly!')
            self.summa.setStyleSheet("font: 10pt; color: red;")



# Окно для добавления расхода
class ENAddExpenditure(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox2 = QtWidgets.QHBoxLayout()

        # Создаём заголовок
        self.title = QtWidgets.QLabel('Add Expense:')
        self.title.setStyleSheet("font: 18pt")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        # Заголовок предществующий введению суммы
        self.summa = QtWidgets.QLabel('Total:')
        self.summa.setStyleSheet("font: 10pt")
        # Поле ввода суммы
        self.editSumma = QtWidgets.QLineEdit()
        self.editSumma.setStyleSheet("font: 9pt")

        # Заголовок предществующий введению описания
        self.description = QtWidgets.QLabel('Description:')
        self.description.setStyleSheet("font: 10pt")
        # Поле ввода описания
        self.editDescription = QtWidgets.QLineEdit()
        self.editDescription.setStyleSheet("font: 9pt")

        # Кнопка для сохранения операции
        self.save = QtWidgets.QPushButton('Save')
        self.save.clicked.connect(self.addExpenditure)
        self.save.setFixedSize(150, 40)
        self.save.setStyleSheet("font: 9pt")

        # Кнопка для очистки полей
        self.delete = QtWidgets.QPushButton('Clear')
        self.delete.clicked.connect(self.clear)
        self.delete.setFixedSize(150, 40)
        self.delete.setStyleSheet("font: 9pt")

        # Кнопка для закрытия окна
        self.btn_close = QtWidgets.QPushButton('Close')
        self.btn_close.clicked.connect(self.closeWindow)
        self.btn_close.setFixedSize(150, 40)
        self.btn_close.setStyleSheet("font: 9pt")

        # Добавляем всё на слои
        self.hbox1.addWidget(self.save)
        self.hbox1.addWidget(self.delete)

        self.hbox2.addWidget(self.btn_close)

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.summa)
        self.vbox.addWidget(self.editSumma)
        self.vbox.addWidget(self.description)
        self.vbox.addWidget(self.editDescription)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.setLayout(self.vbox)
        # Название окна
        self.setWindowTitle('Add Expense')

    # Функция для очистки полей
    def clear(self):
        self.editSumma.clear()
        self.editDescription.clear()

    # Функция для закрытия окна
    def closeWindow(self):
        self.editSumma.clear()
        self.editDescription.clear()
        Eae.close()

    # Функция для добавление расхода
    def addExpenditure(self):
        # Проверяем на ошибки
        try:
            # Если вс хорошо, оставляем текст обычным
            self.summa.setText('Total:')
            self.summa.setStyleSheet("font: 10pt;")

            # С помощью встроенным функций находим сегодняшнюю дату и записываем её
            date = (QtCore.QDate.currentDate()).toString(QtCore.Qt.ISODate)
            # Считываем сумму операции с поля ввода
            summa = float(self.editSumma.text())
            # Считываем описание операции с поля ввода
            description = self.editDescription.text()

            # Если сумма больше нуля
            if summa > 0:
                # Добавляем данные операции в файл с историей и файл с расходами
                new_data = {'date': date, 'total': summa, 'description': description}
                with open('expenditure.json', encoding='utf8') as f:
                    data = json.load(f)
                    data['expenditure'].append(new_data)
                    with open('expenditure.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=2)

                new_data = {'date': date, 'total': summa, 'description': description, 'type': 'expenditure'}
                with open('history.json', encoding='utf8') as f:
                    data = json.load(f)
                    data['history'].append(new_data)
                    with open('history.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=2)

                # Добавляем новую ячейку в скролле истории
                self.cell = QtWidgets.QGroupBox(date)

                self.total_lbl = QtWidgets.QLabel('- ' + str(summa))
                self.desc_lbl = QtWidgets.QLabel(description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                Emw.layout_history.addWidget(self.cell)

                # Добавляем новую ячейку в скролле истории
                self.cell = QtWidgets.QGroupBox(date)

                self.total_lbl = QtWidgets.QLabel('- ' + str(summa))
                self.desc_lbl = QtWidgets.QLabel(description)

                self.vbox_story = QtWidgets.QVBoxLayout()
                self.vbox_story.addWidget(self.total_lbl)
                self.vbox_story.addWidget(self.desc_lbl)

                self.cell.setLayout(self.vbox_story)
                mw.layout_history.addWidget(self.cell)

                # Вычитаем и добавляем сумму расхода в основной вкладке и вкладке с раходами
                Emw.amount -= summa
                Emw.total_main.setText(str(Emw.amount) + ' ₽')
                Emw.amount_expenditure += summa
                Emw.total_expenditure.setText('- ' + str(Emw.amount_expenditure) + ' ₽')
                mw.amount -= summa
                mw.total_main.setText(str(Emw.amount) + ' ₽')
                mw.amount_expenditure += summa
                mw.total_expenditure.setText('- ' + str(Emw.amount_expenditure) + ' ₽')
            # Если сумма меньше нуля, то выводим ошибку и подсвечиваем красным
            else:
                self.summa.setText('Total: The number cannot be less than 0!')
                self.summa.setStyleSheet("font: 10pt; color: red;")
        # Если введены не числовые данные, то выводим ошибку и подсвечиваем красным
        except ValueError:
            self.summa.setText('Total: The data is entered incorrectly!')
            self.summa.setStyleSheet("font: 10pt; color: red;")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    ai = AddIncome()
    ae = AddExpenditure()
    Emw = ENMainWindow()
    Eai = ENAddIncome()
    Eae = ENAddExpenditure()
    mw.show()
    sys.exit(app.exec_())