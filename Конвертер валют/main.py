import tkinter as tk  # Импортируем библиотеку tkinter для создания графического интерфейса
from tkinter import ttk, messagebox  # Импортируем дополнительные модули из tkinter
import requests  # Импортируем библиотеку requests для выполнения HTTP-запросов
from count import countries  # Импортируем словарь с валютами и странами из файла count

currencies_countries = countries  # Инициализируем словарь с валютами и странами

# Функция для получения обменного курса между двумя валютами
def get_exchange_rate(base_currency, target_currency):
    base_currency = base_currency[:3]  # Получаем только первые три буквы исходной валюты
    target_currency = target_currency[:3]  # Получаем только первые три буквы целевой валюты
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"  # Формируем URL для API
    response = requests.get(url)  # Выполняем GET-запрос к API

    if response.status_code == 200:  # Если запрос успешен
        data = response.json()  # Парсим JSON-ответ
        exchange_rate = data['rates'].get(target_currency)  # Получаем курс обмена
        if exchange_rate:
            return exchange_rate  # Возвращаем курс обмена
        else:
            return "Целевая валюта не найдена"  # Ошибка, если целевая валюта не найдена
    else:
        return "Ошибка при получении данных"  # Ошибка, если запрос не успешен

# Функция для конвертации валюты
def convert_currency():
    base_currency = base_currency_var.get().upper()  # Получаем исходную валюту
    target_currency = target_currency_var.get().upper()  # Получаем целевую валюту

    try:
        amount_str = entry_amount.get().replace(',', '.')  # Получаем сумму и заменяем запятую на точку
        amount = float(amount_str)  # Преобразуем строку в число
        exchange_rate = get_exchange_rate(base_currency, target_currency)  # Получаем курс обмена
        
        if amount <= 0:
            messagebox.showerror("Ошибка", "Введите положительное значение")  # Ошибка, если сумма <= 0
        elif type(exchange_rate) == float:
            converted_amount = amount * exchange_rate  # Вычисляем сконвертированную сумму
            converted_amount = round(converted_amount, 3)  # Округляем до 3 знаков после запятой
            messagebox.showinfo("Результат конвертации",
                                f"{amount} {base_currency} равно {converted_amount:.3f} {target_currency}")  # Выводим результат
        else:
            messagebox.showerror("Ошибка", exchange_rate)  # Ошибка, если курс обмена не найден
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числовое значение для суммы")  # Ошибка, если введено не число

# Функция для получения списка валют и стран
def get_currencies_and_countries():
    currencies_with_countries = [f"{currency} - {currencies_countries[currency]}" for currency in currencies_countries]
    return currencies_with_countries  # Возвращаем список валют и стран

# Функция для фильтрации валют по вводу пользователя
def filter_currencies(event, combobox, var):
    search_term = var.get().lower()  # Получаем поисковый запрос в нижнем регистре
    filtered_currencies = [f"{currency} - {currencies_countries[currency]}"
                           for currency in currencies_countries
                           if search_term in currencies_countries[currency].lower() or search_term in currency.lower()]
    
    cursor_pos = combobox.index(tk.INSERT)  # Получаем текущую позицию курсора в combobox
    current_text = combobox.get()  # Получаем текущий текст в combobox
    
    combobox['values'] = filtered_currencies  # Обновляем значения combobox
    combobox.set(current_text)  # Устанавливаем обратно текущий текст
    
    combobox.icursor(cursor_pos)  # Устанавливаем курсор обратно на его текущую позицию
    combobox.selection_range(cursor_pos, cursor_pos)  # Выделяем текст от текущей позиции до текущей позиции

# Функция для очистки текста в поле ввода при фокусировке
def clear_entry_text(event):
    if entry_amount.get() == "Введите сумму":
        entry_amount.delete(0, 'end')  # Удаляем текст в поле ввода

# Создаем основное окно приложения
root = tk.Tk()
root.title("Конвертер валют")  # Устанавливаем заголовок окна
root.geometry("600x400")  # Устанавливаем размеры окна
root.resizable(False, False)  # Запрещаем изменение размеров окна

style = ttk.Style()
style.theme_use('clam')  # Устанавливаем тему оформления виджетов

root.configure(bg='#b591b5')  # Устанавливаем цвет фона для главного окна
style.configure('TFrame', background='#b591b5')  # Устанавливаем цвет фона для фреймов
style.configure('TLabel', background='#b591b5', foreground='white', font=('Helvetica', 12))  # Настраиваем стиль для меток
style.configure('TButton', background='#0078D7', foreground='white', font=('Helvetica', 12, 'bold'))  # Настраиваем стиль для кнопок
style.configure('TCombobox', fieldbackground='#f0f0f0', background='#f0f0f0', font=('Helvetica', 12))  # Настраиваем стиль для комбобоксов
style.configure('TEntry', font=('Helvetica', 12))  # Настраиваем стиль для полей ввода

mainframe = ttk.Frame(root, padding="20 20 20 20")  # Создаем главный фрейм с отступами
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))  # Размещаем фрейм на главном окне, растягивая на все стороны
mainframe.columnconfigure(0, weight=1)  # Настраиваем растягивание столбца
mainframe.rowconfigure(0, weight=1)  # Настраиваем растягивание строки

base_currency_var = tk.StringVar()  # Переменная для выбранной исходной валюты
base_currency_label = ttk.Label(mainframe, text="Исходная валюта:")  # Метка для выбора исходной валюты
base_currency_label.grid(column=1, row=1, sticky=tk.W, padx=10, pady=10)  # Размещаем метку на главном фрейме

base_currency_combobox = ttk.Combobox(mainframe, textvariable=base_currency_var, state='normal', width=40)  # Комбобокс для выбора исходной валюты
base_currency_combobox.grid(column=2, row=1, sticky=tk.W, padx=10, pady=10)  # Размещаем комбобокс на главном фрейме
base_currency_combobox['values'] = get_currencies_and_countries()  # Устанавливаем значения для комбобокса
base_currency_combobox.set("Выберите валюту")  # Устанавливаем начальное значение
base_currency_combobox.bind("<KeyRelease>", lambda event: filter_currencies(event, base_currency_combobox, base_currency_var))  # Привязываем фильтрацию к вводу

# Создаем переменную для выбранной целевой валюты
target_currency_var = tk.StringVar()
# Создаем метку для отображения текста "Целевая валюта:" на главном фрейме
target_currency_label = ttk.Label(mainframe, text="Целевая валюта:")
# Размещаем метку на главном фрейме, устанавливаем выравнивание, отступы
target_currency_label.grid(column=1, row=2, sticky=tk.W, padx=10, pady=10)
# Создаем комбобокс для выбора целевой валюты, устанавливаем переменную для связи с текстом, состояние и ширину
target_currency_combobox = ttk.Combobox(mainframe, textvariable=target_currency_var, state='normal', width=40)
# Размещаем комбобокс на главном фрейме, устанавливаем выравнивание, отступы и 
target_currency_combobox.grid(column=2, row=2, sticky=tk.W, padx=10, pady=10)
# Устанавливаем значения для комбобокса целевой валюты на основе функции получения валют и стран
target_currency_combobox['values'] = get_currencies_and_countries()
# Устанавливаем начальное значение в комбобоксе целевой валюты
target_currency_combobox.set("Выберите валюту")
# Привязываем обработчик события KeyRelease к комбобоксу для фильтрации валют
target_currency_combobox.bind("<KeyRelease>", lambda event: filter_currencies(event, target_currency_combobox, target_currency_var))

# Создаем метку для отображения текста "Сумма для конвертации:" на главном фрейме
amount_label = ttk.Label(mainframe, text="Сумма для конвертации:")
# Размещаем метку на главном фрейме, устанавливаем выравнивание, отступы и паддинги
amount_label.grid(column=1, row=3, sticky=tk.W, padx=10, pady=10)
# Создаем поле ввода для ввода суммы для конвертации, устанавливаем ширину
entry_amount = ttk.Entry(mainframe, width=43)
# Размещаем поле ввода на главном фрейме, устанавливаем выравнивание, отступы и паддинги
entry_amount.grid(column=2, row=3, sticky=tk.W, padx=10, pady=10)
# Устанавливаем начальный текст в поле ввода суммы
entry_amount.insert(0, "Введите сумму")
# Привязываем обработчик события FocusIn к полю ввода для очистки начального текста при фокусировке
entry_amount.bind("<FocusIn>", clear_entry_text)

# Создаем кнопку "Конвертировать" с командой на вызов функции convert_currency
convert_button = ttk.Button(mainframe, text="Конвертировать", command=convert_currency)
# Размещаем кнопку на главном фрейме, устанавливаем выравнивание, отступы и паддинги
convert_button.grid(column=2, row=4, sticky=tk.W, padx=10, pady=20)

# Проходимся по всем дочерним элементам главного фрейма и настраиваем отступы
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Устанавливаем фокус на поле ввода суммы для конвертации при запуске
entry_amount.focus()

# Функция для обработки закрытия окна
def on_closing():
    # Отображаем диалоговое окно с подтверждением выхода
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
        root.destroy()  # Закрываем главное окно приложения

# Привязываем обработчик закрытия окна к событию WM_DELETE_WINDOW
root.protocol("WM_DELETE_WINDOW", on_closing)
# Запускаем главный цикл обработки событий
root.mainloop()