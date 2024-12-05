import holidays

def get_holiday(date):
    vn_holidays = holidays.Vietnam()
    holiday = vn_holidays.get(date)
    if not holiday:
        return "Normal Day"
    return holiday


if __name__ == "__main__":
    print(get_holiday("2021-01-01"))  # New Year's Day
    print(get_holiday("2021-01-02"))  # Normal Day