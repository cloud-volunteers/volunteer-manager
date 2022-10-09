from pandas import ExcelFile, read_excel, DataFrame
from hashlib import md5
from datetime import date

def email_generator(n):
    return f"{str(md5(str(n).encode('ascii')).hexdigest())}@email.com"

def get_required_values(value, required):
    return bool(len([word for word in required if word in str(value)]))

def process_excel(file):
    xls = ExcelFile(file)
    df = read_excel(xls, 'Responses')

    output_df = DataFrame()

    output_df['email'] = df.index
    output_df['email'] = output_df['email'].apply(email_generator)
    output_df['county'] = df['County']
    output_df['online'] = df.apply(lambda x: get_required_values(x['How do you want to work with children'], ['Online']), axis=1)
    output_df['offline'] = df.apply(lambda x: get_required_values(x['How do you want to work with children'], ['Offline', 'Doar FIZIC']), axis=1)
    output_df['age'] = df['Age']

    output_df['Monday'] = df.apply(lambda x: get_required_values(x['Schedule - day'], ['Monday', 'Week days', 'Both']), axis=1)
    output_df['Tuesday'] = df.apply(lambda x: get_required_values(x['Schedule - day'], ['Tuesday', 'Week days', 'Both']), axis=1)
    output_df['Wednesday'] = df.apply(lambda x: get_required_values(x['Schedule - day'], ['Wednesday', 'Week days', 'Both']), axis=1)
    output_df['Thursday'] = df.apply(lambda x: get_required_values(x['Schedule - day'], ['Thursday', 'Week days', 'Both']), axis=1)
    output_df['Friday'] = df.apply(lambda x: get_required_values(x['Schedule - day'], ['Friday', 'Week days', 'Both']), axis=1)
    output_df['Saturday'] = df.apply(lambda x: get_required_values(x['Schedule - day'], ['Saturday', 'Weekend', 'Both']), axis=1)
    output_df['Sunday'] = df.apply(lambda x: get_required_values(x['Schedule - day'], ['Sunday', 'Weekend', 'Both']), axis=1)

    output_df['09:00 - 12:00'] = df.apply(lambda x: get_required_values(x['Schedule - hours'], ['09:00 - 12:00']), axis=1)
    output_df['14:00 - 16:00'] = df.apply(lambda x: get_required_values(x['Schedule - hours'], ['16:00 - 19:00']), axis=1)
    output_df['16:00 - 19:00'] = df.apply(lambda x: get_required_values(x['Schedule - hours'], ['16:00 - 19:00']), axis=1)

    output_df['reading_and_writing_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['Help with reading and writing']), axis=1)
    output_df['romanian_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['Romanian']), axis=1)
    output_df['math_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['Math']), axis=1)
    output_df['chemistry_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['Chemistry']), axis=1)
    output_df['history_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['History']), axis=1)
    output_df['physics_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['Physics']), axis=1)
    output_df['biology_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['Biology']), axis=1)
    output_df['french_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['French']), axis=1)
    output_df['geography_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['Geography']), axis=1)
    output_df['english_homework'] = df.apply(lambda x: get_required_values(x['School tutoring and homework'], ['English']), axis=1)

    output_df['romanian_8th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Romanian-8th grade']), axis=1)
    output_df['romanian_12th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Romanian-12th grade']), axis=1)
    output_df['math_8th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Math-8th grade']), axis=1)
    output_df['math_12th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Math-12th grade']), axis=1)
    output_df['physics_12th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Physics - 12th grade']), axis=1)
    output_df['chemistry_12th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Chemistry- 12th grade']), axis=1)
    output_df['geography_12th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Geography - 12th grade']), axis=1)
    output_df['biology_12th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Biology - 12th grade']), axis=1)
    output_df['sociology_12th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['Sociology - 12th grade']), axis=1)
    output_df['history_12th_grade_exam'] = df.apply(lambda x: get_required_values(x['Tutoring for final exams'], ['History - 12th grade']), axis=1)

    output_df['vocational_counseling_workshops'] = df.apply(lambda x: get_required_values(x['Other educative activities'], ['Vocational counseling']), axis=1)
    output_df['online_safety_workshops'] = df.apply(lambda x: get_required_values(x['Other educative activities'], ['Online safety workshops']), axis=1)
    output_df['games_and_personal_development_activities_workshops'] = df.apply(lambda x: get_required_values(x['Other educative activities'], ['Games and personal development activities']), axis=1)
    output_df['mentorship_for_teenagers_workshops'] = df.apply(lambda x: get_required_values(x['Other educative activities'], ['Mentorship for teenagers']), axis=1)
    output_df['health_education_workshops'] = df.apply(lambda x: get_required_values(x['Other educative activities'], ['Health education workshops']), axis=1)
    output_df['financial_education_workshops'] = df.apply(lambda x: get_required_values(x['Other educative activities'], ['Financial education workshops']), axis=1)
    output_df['civic_education_workshops'] = df.apply(lambda x: get_required_values(x['Other educative activities'], ['Civic education workshops']), axis=1)
    output_df['how_to_use_the_computer_workshops'] = df.apply(lambda x: get_required_values(x['Other educative activities'], ['"How to use the computer" workshops']), axis=1)

    return output_df.to_dict('records')

def json_default(value):
    if isinstance(value, date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
def parse_weekdays(input):
    output = {}
    for weekday in DAYS:
        output[weekday] = False
    for day in str(input).split(","):
        day = day.strip()
        if day == 'nan':
            return output
        elif day == 'Both':
            for weekday in DAYS:
                output[weekday] = True
        elif day == 'Week days':
            for weekday in DAYS[:5]:
                output[weekday] = True
            return output
        elif day == 'Weekend':
            for weekday in DAYS[5:]:
                output[weekday] = True
            return output
        elif day in DAYS:
            output[day] = True
    return output

HOURS = ['09:00 - 12:00', '14:00 - 16:00', '16:00 - 19:00']
def parse_hours(input):
    output = {}
    for slot_hour in HOURS:
        output[slot_hour.replace(" ","")] = False
    for hour in str(input).split(","):
        hour = hour.strip()
        for slot_hour in HOURS:
            if slot_hour in hour:
                output[slot_hour.replace(" ","")] = True
    return output