from datetime import datetime, timedelta

# Constants for the Raddinian Calendar
RADDINIAN_EPOCH_START = datetime(2025, 1, 23)  # 1 Lexember, 1 A.L.
RADDINIAN_MONTHS = [
    "Lexember", "Objectiontide", "Margust", "Precedentis", "Tribunalis",
    "Statutember", "Veritober", "Lawvember", "Perennus", "Temporalis Rescriptum"
]
RADDINIAN_WEEKDAYS = [
    "Gavelsday", "Motionsday", "Jurisday", "Oathday", "Dictumsday",
    "Veriday", "Saulsday", "Lexday", "Praetorday", "Clownsday"
]
DAYS_PER_MONTH = [40, 40, 40, 40, 40, 40, 40, 40, 40, 5]  # Temporalis Rescriptum starts with 5 days
DAYS_PER_WEEK = 10
CYCLE_LENGTH = sum(DAYS_PER_MONTH)  # 365 days

# Function to determine if a year is a leap year in Raddinian time
def is_leap_year(year):
    if year <= 0:
        return False  # No leap years before 1 A.L.
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        if year % 3216 == 0:
            return False  # Skip a leap year every 3,216 years
        return True
    return False

# Function to get extra leap days every 10,000 years
def get_leap_days(year):
    leap_days = 1 if is_leap_year(year) else 0
    if year % 10000 == 0:
        leap_days += 1  # Extra correction day every 10,000 years
    return leap_days

# Convert Raddinian to Gregorian
def radd_greg(day: int, month: int, year: int) -> str:
    total_days = 0
    if year > 0:  # A.L. handling
        for y in range(1, year):
            total_days += CYCLE_LENGTH + get_leap_days(y)
    else:  # B.J. handling
        for y in range(-1, year, -1):
            total_days -= CYCLE_LENGTH
    leap_days = get_leap_days(year)
    if month == 10:  # Temporalis Rescriptum
        max_days = DAYS_PER_MONTH[9] + leap_days
        if day > max_days:
            raise ValueError(f"Invalid day {day} in Temporalis Rescriptum {year} (Max: {max_days})")
        total_days += sum(DAYS_PER_MONTH[:9]) + leap_days + (day - 1)
    else:
        total_days += sum(DAYS_PER_MONTH[:month - 1]) + (day - 1)
    
    try:
        g_date = RADDINIAN_EPOCH_START + timedelta(days=total_days)
        return g_date.strftime("%B %d, %Y A.D." if g_date.year > 0 else "%B %d, %Y B.C.")
    except OverflowError:
        return "Error: Python can only reckon Gregorian dates between 1-9999 A.D."

# Convert Gregorian to Raddinian
def greg_radd(day: int, month: int, year: int) -> str:
    g_date = datetime(year, month, day)
    delta_days = (g_date - RADDINIAN_EPOCH_START).days
    if delta_days >= 0:
        era = "A.L."
        r_year = 1
        while delta_days >= CYCLE_LENGTH + get_leap_days(r_year):
            leap_days = get_leap_days(r_year)
            delta_days -= (CYCLE_LENGTH + leap_days)
            r_year += 1
    else:
        era = "B.J."
        r_year = -1
        delta_days = -delta_days
        while delta_days > CYCLE_LENGTH:
            delta_days -= CYCLE_LENGTH
            r_year -= 1
        delta_days = CYCLE_LENGTH - delta_days
    r_month = 1
    leap_days = get_leap_days(r_year)
    for i, days in enumerate(DAYS_PER_MONTH):
        if i == 9:
            days += leap_days
        if delta_days < days:
            r_day = delta_days + 1
            break
        delta_days -= days
        r_month += 1
    return f"{r_day} {RADDINIAN_MONTHS[r_month - 1]}, {abs(r_year)} {era}"

__all__ = ["radd_greg", "greg_radd", "is_leap_year", "get_leap_days"]
