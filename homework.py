import datetime as dt


""" Создаём общий ксласс для всех калькуляторов """


class Calculator:
    delta = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        self.today = dt.datetime.now().date()
        return sum(record.amount for record in
                   self.records if record.date == self.today)

    def get_week_stats(self):
        self.today = dt.datetime.now().date()
        week_stats = 0
        first_date = self.today - self.delta
        for record in self.records:
            if first_date < record.date <= self.today:
                week_stats += record.amount
        return week_stats


""" Создаём класс для удобства создания записей """


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()


""" Создаём класс для калькулятора калорий """


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        remained = self.limit - today_stats
        if today_stats < self.limit:
            return ("Сегодня можно съесть что-нибудь ещё, "
                    f"но с общей калорийностью не более {remained} кКал")
        else:
            return "Хватит есть!"


""" Создаём класс для калькулятора денег """


class CashCalculator(Calculator):
    USD_RATE = 77.11
    EURO_RATE = 90.81

    def get_today_cash_remained(self, currency):
        currencyes = {
            'rub': [1.0, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro']
            }
        remained = ((self.limit - self.get_today_stats())
                    / currencyes[currency][0])
        remained = round(remained, 2)
        if remained > 0:
            return f"На сегодня осталось {remained} {currencyes[currency][-1]}"
        elif remained == 0:
            return "Денег нет, держись"
        else:
            return ("Денег нет, держись: твой долг - "
                    f"{abs(remained)} {currencyes[currency][-1]}")
