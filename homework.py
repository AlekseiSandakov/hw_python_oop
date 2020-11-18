import datetime as dt


class Calculator:
    """ Создаём общий ксласс для всех калькуляторов """
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
        first_date = self.today - self.delta
        return sum(record.amount for record in
                   self.records if first_date < record.date <= self.today)

    def get_remained(self):
        remained = self.limit - self.get_today_stats()
        return remained


class Record:
    """ Создаём класс для удобства создания записей """
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()


class CaloriesCalculator(Calculator):
    """ Создаём класс для калькулятора калорий """
    def get_calories_remained(self):
        if self.get_today_stats() < self.limit:
            return ("Сегодня можно съесть что-нибудь ещё, но с общей "
                    f"калорийностью не более {self.get_remained()} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    """ Создаём класс для калькулятора денег """
    USD_RATE = 75.93
    EURO_RATE = 90.23

    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': [1.0, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro']
            }
        cur_rate, cur_title = currencies[currency]
        if self.get_remained() == 0:
            return "Денег нет, держись"
        remained = round((self.get_remained()/cur_rate), 2)
        if remained > 0:
            return f"На сегодня осталось {remained} {cur_title}"
        else:
            return ("Денег нет, держись: твой долг - "
                    f"{abs(remained)} {cur_title}")
