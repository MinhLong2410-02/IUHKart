from datetime import datetime
import holidays

def get_holiday(date):
    vn_holidays = holidays.Vietnam()
    holiday = vn_holidays.get(date)
    if not holiday:
        return "Normal Day"
    return holiday

def parse_date(date_str:str) -> dict:
    _id = int(date_str.replace('-', ''))
    date = datetime.strptime(date_str,  "%Y-%m-%d")
    return {
        'id': _id,
        'full_date': date_str,
        'day': date.day,
        'month': date.month,
        'year': date.year,
        'quarter': (date.month - 1) // 3 + 1,
        'day_of_week': date.weekday(),
        'week_of_year': date.isocalendar()[1],
        'is_weekend': date.weekday() in [5, 6],
        'is_holiday': get_holiday(date_str)
    }

if __name__ == "__main__":
    res = parse_date("2024-12-06")
    print(res)


# {'id': 20241206, 'full_date': '2024-12-06', 'day': 6, 'month': 12, 'year': 2024, 'quarter': 4, 'day_of_week': 4, 'week_of_year': 49, 'is_weekend': False, 'is_holiday': 'Normal Day'}