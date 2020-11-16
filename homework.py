import datetime as dt

# Создаём общий ксласс для всех калькуляторов
class Calculator:
    today = dt.datetime.now().date()
    delta = dt.timedelta(days=7)
    def __init__(self, limit):
        self.limit = limit
        self.records = []
    def add_record(self, record):
        self.records.append(record)
    def get_today_stats(self):
        today_stats = 0
        for record in self.records:
            if record.date == self.today:
                today_stats += record.amount
        return today_stats
    def get_week_stats(self):
        week_stats = 0
        first_date = self.today - self.delta
        for record in self.records:
            if first_date < record.date <= self.today:
                week_stats += record.amount
        return week_stats

# Создаём класс для удобства создания записей
class Record:
    date_format = '%d.%m.%Y'
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.date = dt.datetime.strptime(date, self.date_format).date() if date else dt.datetime.now().date()
        self.comment = comment

# Создаём класс для калькулятора калорий
class CaloriesCalculator(Calculator):
    def add_record(self, record):
        super().add_record(record)
    def get_today_stats(self):
        super().get_today_stats()
    def get_calories_remained(self):
        day_calories = super().get_today_stats()
        diff = self.limit - day_calories
        if day_calories < self.limit:
            return (f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {diff} кКал")
        else:
            return ("Хватит есть!")
        super().get_week_stats(self)

# Создаём класс для калькулятора денег
class CashCalculator(Calculator):
    USD_RATE = 77.11
    EURO_RATE = 90.81
    def add_record(self, record):
        super().add_record(record)
    def get_today_stats(self):
        super().get_today_stats()
    def get_today_cash_remained(self, currency):
        today_stats = super().get_today_stats()
        remained = self.limit - today_stats
        currency_title = ""
        if currency == "usd":
            remained /= self.USD_RATE
            currency_title = "USD"
        elif currency == "eur":
            remained /= self.EURO_RATE
            currency_title = "Euro"
        elif currency == "rub":
            currency_title = "руб"
        remained = round(remained, 2)
        if remained > 0:
            return f"На сегодня осталось {remained} {currency_title}"
        elif remained == 0:
            return "Денег нет, держись"
        else:
            return f"Денег нет, держись: твой долг - {-remained} {currency_title}"
    def get_week_stats(self):
        super().get_week_stats(self)