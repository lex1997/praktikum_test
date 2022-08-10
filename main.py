import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # Нужно прописать документацию для этого метода и всех остальных методов во всех классах этого модуля
        # чтобы было удобнее работать.
        # Удобнее как другим разработчикам, так и тебе.
        # Для лучшего понимания изучи и делай как описано: https://peps.python.org/pep-0257/
        # Для создания шаблона документации вставь """ в следующей строке и нажми Enter.
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            # в наименовании переменной Record лучше не использовать uppercase, лучше только lowercase
            # чтобы не путать например с названием класса
            # Для лучшего понимания изучи https://pythonchik.ru/osnovy/imenovanie-v-python
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
                # Это условие можно написать более коротко: 7 > (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # вместо комментария выше должна быть документация
        # но при небходимости написания комментария лучше использовать формат
        # который описа здесь:
        # https://softwareengineering.stackexchange.com/questions/315792/best-way-of-writing-comments-in-code
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
            # Внутри первой строки нет переменных, поэтому f-строка не нужна
            # Не нужно делать перенос бэкслешем лучше возвращать значения строк другим методом
            # например присвоение этих строк в переменные и объединять эти переменные в return с помощью +
        else:
            return('Хватит есть!') # Здесь не требуются () и нужен пробел между return и его объектом


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    # Переменные нельзя называть в uppercase + их можно было объявить внутри метода get_today_cash_remained
    # поскольку они используются только там, и не пришлось бы присваивать их на входных параметрах
    # Для лучшего понимания изучи https://pythonchik.ru/osnovy/imenovanie-v-python

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Аргументы функции тоже должны быть в lowercase
        # Для лучшего понимания изучи https://pythonchik.ru/osnovy/imenovanie-v-python
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            # строка 90 не требуется, по сути она бесполезна для подобного кейса лучше использовать функцию float()
            currency_type = 'руб' # ниже желательно оставить пустую строку
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # Нужно придерживаться единого стандарта в return подобно тому который реализован выше
        # из всех он самый корректный
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
        # Не нужно делать перенос бэкслешем лучше возвращать значения строк другим методом
        # например присвоение этих строк в переменные и объединять эти переменные в return

    def get_week_stats(self):
        super().get_week_stats()
        # во-первых отсутствует return у метода, когда в методе предка он есть
        # во-вторых этот метод в принципе не нужен поскольку он уже имеется у родительского класса
        # а дочерний класс может спокойно его использовать


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
calories_calculator = CaloriesCalculator(2000)
# дата в параметрах не указана,
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе"))
calories_calculator.add_record(Record(amount=70, comment="кофе"))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300.25, comment="Серёге за обед"))
calories_calculator.add_record(Record(amount=600, comment="обед с Серёгай"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
cash_calculator.add_record(Record(amount=1000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained("rub"))
print(calories_calculator.get_calories_remained())
# должно напечататься
# На сегодня осталось 555 руб

