from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import re


def parse_date_expression(expression):
    today = datetime.now()
    print(expression)
    # Mapping of words to numbers
    words_to_numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "week": 7, "weeks": 7, "month": 30, "months": 30,
        "quarter": 90, "quarters": 90,
        "mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6,
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
        "year": 365, "years": 365
    }

    # Convert to lowercase for case-insensitive comparison
    expression = expression.lower()

    if "last" in expression or "past" in expression:
        if "month" in expression:
            last_month = today.replace(day=1) - timedelta(days=1)
            return last_month.replace(day=1)
        elif any(day in expression for day in words_to_numbers.keys()):
            weekday = [day for day in words_to_numbers.keys()
                       if day in expression][0]
            past_occurrence = today - timedelta(days=(today.weekday() + 7))
            days_until_last = (past_occurrence.weekday() -
                               words_to_numbers[weekday]) % 7
            return past_occurrence - timedelta(days=days_until_last)
        elif "week" in expression:
            return today - timedelta(days=(today.weekday() + 7))
        elif "quarter" in expression:
            current_month = today.month
            last_quarter_month = ((current_month - 1) // 3) * 3 + 1
            this_quarter_start = today.replace(month=last_quarter_month, day=1)
            if today.month % 3 == 0:
                this_quarter_start -= relativedelta(months=3)
            return this_quarter_start

    if "next" in expression:
        if any(day in expression for day in words_to_numbers.keys() if day != "next"):
            weekday = [day for day in words_to_numbers.keys(
            ) if day != "next" and day in expression][0]
            next_occurrence = today + timedelta(days=(7 - today.weekday()) % 7)
            days_until_next = (
                words_to_numbers[weekday] - next_occurrence.weekday()) % 7
            return next_occurrence + timedelta(days=days_until_next)
        elif "week" in expression:
            next_week = today + timedelta(days=(7 - today.weekday()))
            return next_week + timedelta(days=7)
        elif "month" in expression:
            return today.replace(day=1) + relativedelta(months=1)
        elif "quarter" in expression:
            current_month = today.month
            next_quarter_month = ((current_month - 1) // 3 + 1) * 3 + 1
            next_quarter_start = today.replace(month=next_quarter_month, day=1)
            if today.month % 3 == 0:
                next_quarter_start += relativedelta(months=3)
            return next_quarter_start
        elif "to next" in expression:
            next_monday = today + timedelta(days=(7 - today.weekday()))
            return next_monday + timedelta(days=7)
        else:
            next_occurrence = today + timedelta(days=(7 - today.weekday()))
            return next_occurrence + timedelta(days=1)

    if "last" in expression:
        if "month" in expression:
            last_month = today.replace(day=1) - timedelta(days=1)
            return last_month.replace(day=1)
        else:
            return today - timedelta(days=(today.weekday() + 7))

    if "end of" in expression:
        print(expression)
        if "week" in expression:
            end_of_week = today + timedelta(days=(6 - today.weekday()))
            return end_of_week.replace(hour=23, minute=59, second=59)
        elif "month" in expression:
            print("true")
            return today.replace(day=1) + relativedelta(months=2) - timedelta(days=1)
        elif "quarter" in expression:
            current_month = today.month
            next_quarter_month = ((current_month - 1) // 3 + 1) * 3 + 1
            return today.replace(month=next_quarter_month, day=1) + relativedelta(months=2) - timedelta(days=1)

    if "in" in expression or "ago" in expression:
        words = expression.split()
        if words[0].isdigit():
            days_offset = int(words[0])
            if words[1] in words_to_numbers:
                days_offset *= words_to_numbers[words[1]]
            elif words[1] == "year":
                days_offset *= 365
            else:
                raise ValueError("Invalid expression: Unknown time unit")
            if "ago" in expression:
                days_offset = -days_offset
            return today + timedelta(days=days_offset)
        else:
            if words[1] in words_to_numbers:
                days_offset = words_to_numbers[words[1]]
            else:
                raise ValueError("Invalid expression: Unknown time unit")
            return today + timedelta(days=days_offset)

    # If the expression is just a date, parse it using dateutil
    try:
        return parse(expression, fuzzy=True)
    except ValueError:
        raise ValueError("Invalid date expression")


def replace_date_expressions(text):

    date_expressions1 = [
        "next tue",
        "next wed",
        "next fri",
        "last month",
        "24may",
        "end of next week",
        "end of next month",
        "end of next quarter",
        "in three days",
        "in five days",
        "next week",
        "next month",
        "next monday",
        "next to next monday",
        "3 days later",
        "before the end of next month",
        "two weeks ago",
        'next quarter',
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun",
        "last month",
        'end of month'
    ]

    date_formats = [
        "24 May 2024",
        "May 24, 2024",
        "2024-05-24",
        "05/24/2024",
        "24.05.2024"
    ]

    date_words = [
        "Mon", "Monday",
        "Tue", "Tuesday",
        "Wed", "Wednesday",
        "Thu", "Thursday",
        "Fri", "Friday",
        "Sat", "Saturday",
        "Sun", "Sunday"
    ]

    date_expressions2 = [
        "Next Monday",
        "Next Tuesday",
        "Next Wednesday",
        "Next Thursday",
        "Next Friday",
        "Next Saturday",
        "Next Sunday",
        "Next week",
        "Next month",
        "Next quarter",
        "Next year",
        "Last Monday",
        "Last Tuesday",
        "Last Wednesday",
        "Last Thursday",
        "Last Friday",
        "Last Saturday",
        "Last Sunday",
        "Last week",
        "Last month",
        "Last quarter",
        "Last year",
        "Past Monday",
        "Past Tuesday",
        "Past Wednesday",
        "Past Thursday",
        "Past Friday",
        "Past Saturday",
        "Past Sunday",
        "Past week",
        "Past month",
        "Past quarter",
        "Past year",
        "Two weeks ago",
        "Three weeks ago",
        "Two months ago",
        "Three months ago",
        "Two quarters ago",
        "Three quarters ago",
        "Two years ago",
        "Three years ago",
        "End of next week",
        "End of next month",
        "End of next quarter",
        "End of next year",
        "In three days",
        "In five days",
        "In one week",
        "In two weeks",
        "In one month",
        "In two months",
        "In one quarter",
        "In two quarters",
        "In one year",
        "In two years",
        "Before the end of next week",
        "Before the end of next month",
        "Before the end of next quarter",
        "Before the end of next year",
        "After the end of next week",
        "After the end of next month",
        "After the end of next quarter",
        "After the end of next year",
        "Next to next Monday",
        "Next to next Tuesday",
        "Next to next Wednesday",
        "Next to next Thursday",
        "Next to next Friday",
        "Next to next Saturday",
        "Next to next Sunday",
        "Next to next week",
        "Next to next month",
        "Next to next quarter",
        "Next to next year"
    ]

    date_expressions = date_formats + date_words + \
        date_expressions1 + date_expressions2
    date_expressions = list(set(date_expressions))

    # Sort date expressions by length in descending order to prioritize longer expressions
    date_expressions.sort(key=len, reverse=True)

    for expression in date_expressions:
        # print(expression)
        # Case-insensitive matching
        pattern = re.compile(re.escape(expression), re.IGNORECASE)
        date = parse_date_expression(expression)
        text = pattern.sub(date.strftime("%Y-%m-%d"), text)

    return text

# Example usage
# text = """
# I need the report by next Tue. Last month's sales were impressive.
# The deadline is 24may. Can we discuss this at the End of next week?
# Let's plan the project for the next quarter.
# We'll deliver the project in three days.
# Please submit your proposal in five days.
# The meeting is scheduled for next mon.
# Let's meet next to next Monday to finalize the details.
# I'll get back to you 3 days later.
# We should finish the project before the end of next month.
# The event happened two weeks ago abrakadaba . I paid  this invoice last month.
#
# """


text = 'end of month'
# text = 'end of next week'

updated_text = replace_date_expressions(text)
print(updated_text)
