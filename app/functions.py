from pandas import ExcelFile, read_excel, DataFrame
from secrets import token_hex

def email_generator(n):
    return f"{str(token_hex(16))}@email.com"

def get_required_values(value, required):
    return bool(len([word for word in required if word in value]))

def process_excel(file):
    xls = ExcelFile(file)
    df = read_excel(xls, 'Responses')
    df['Email Address'] = df['Email Address'].apply(email_generator)
    df['Online'] = df.apply(lambda x: get_required_values(x['How do you want to work with children'], ['Online']), axis=1)
    df['Offline'] = df.apply(lambda x: get_required_values(x['How do you want to work with children'], ['Offline', 'Doar FIZIC']), axis=1)

    output_df = DataFrame()

    output_df['email'] = df['Email Address']
    output_df['county'] = df['County']
    output_df['online'] =  df['Online']
    output_df['offline'] = df['Offline']
    output_df['age'] = df['Age']

    return output_df.to_dict('records')
