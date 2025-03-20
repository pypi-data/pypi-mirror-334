import pymsteams
import awswrangler as wr
import pandas as pd
import numpy as np
import sqlalchemy
import datetime
import os
import ast
import boto3
from botocore.exceptions import ClientError
import redshift_connector
import pymysql
import calendar
import requests
import json, re
from sqlalchemy import create_engine, MetaData, text
import pandas_market_calendars as mcal


# def onError(title, destination, assignee, error_message, script_name, script_location):
#     myTeamsMessage = pymsteams.connectorcard(destination)
#     # create the section
#     myMessageSection = pymsteams.cardsection()
#     # Activity Elements
#     myMessageSection.activityTitle(title)
#     myMessageSection.activitySubtitle("production pipeline alert")
#     myMessageSection.activityImage("https://teamsnodesample.azurewebsites.net/static/img/image4.png")
#     # Facts are key value pairs displayed in a list.
#     myMessageSection.addFact("Assignning to", assignee)
#     myMessageSection.addFact("Error Message", error_message)
#     myMessageSection.addFact("Script Name", script_name)
#     myMessageSection.addFact("Script Location", script_location)
#     # Add your section to the connector card object before sending
#     myTeamsMessage.addSection(myMessageSection)
#     myTeamsMessage.summary(title)
#     myTeamsMessage.send()

def onError(title,error_message,assignee,script_name,script_location,destination='info'):
    def safe_for_json(text):
        if not isinstance(text, str):
            return text
            
        # Replace common problematic characters
        text = text.replace('\\', '\\\\')  # Escape backslashes first
        text = text.replace('"', '\\"')    # Escape double quotes
        text = text.replace('\n', '\\n')   # Escape newlines
        text = text.replace('\r', '\\r')   # Escape carriage returns
        text = text.replace('\t', '\\t')   # Escape tabs
        
        # Handle any control characters
        return re.sub(r'[\x00-\x1F\x7F]', '', text)

    alert_data = {
    "title": f"{safe_for_json(title)}",
    "message": f"Message: {safe_for_json(error_message)}",
    "Assigned_to": f"Assigned_to: {safe_for_json(assignee)}",
    "Script_name": f"Script_name: {safe_for_json(script_name)}",
    "Script_location": f"Script_location: {safe_for_json(script_location)}",
    }

    channel=ast.literal_eval(amazon.get_secret(secret_name = "tradeup-teams-alert", region_name = 'us-east-1'))
    if destination=='alert':
        url=channel['alert_url']
    elif destination=='testing':
        url=channel['testing_url']
    else:
        url=channel['info_url']
        
    response = requests.post(url, data=json.dumps(alert_data), headers={'Content-Type': 'application/json'})
    return response



def clear_table(date, table_name=None, db_name=None, user=None, password=None, IP_address=None, port=None):
    db = pymysql.connect(host = IP_address, user = user, passwd = password, database = db_name, port = port, charset='utf8')
    try:
        cursor = db.cursor()
        cursor.execute(f'''
            delete FROM {table_name}
            where Date = '{date}';
                                
        ''')
        db.commit()
        print(f'clear table {table_name}: 1')
    except Exception as e:
        print(e)
    finally:
        db.close()

def insert_db(df=None, table_name=None, db_name=None, user=None, password=None, IP_address=None, port=None):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{IP_address}:{port}/{db_name}")  
    try:
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print(f'{table_name} ingestion: 1')
    except Exception as e:
        raise ValueError(e)
    finally:
        engine.dispose()
        
        
def last_business_day(year, month):
    last_day = calendar.monthrange(year, month)[1]
    day = datetime.date(year, month, last_day)
    while day.weekday() > 4:
        day -= datetime.timedelta(days=1)
    return day


def data_pull(user=None, password=None, IP_address=None, port=None, db_name=None, SQL_query=None):
    try:
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{IP_address}:{port}/{db_name}") 
        query = f"{SQL_query}"

        with engine.connect() as conn:
            data = pd.read_sql_query(sql=query, con=conn.connection)
            return data    
    except Exception as e:
        raise ValueError(e)
    finally:
        engine.dispose()
        

def to_float(series):
    new_lst = []
    lst = list(series)
    for i in lst:
        if i == "" or type(i) == float:
            new_lst.append(np.nan)
        else:
            if "-" in i:
                i = i.replace(",","").replace("-","").replace(" ","")
                i = float(i) * (-1)
                new_lst.append(i)
            else:
                i = i.replace(",","").replace(" ","")
                new_lst.append(float(i))
    return new_lst

class CobolNumericConverter():
    def __init__(self, decimal_digits):
        self.dec_digits = decimal_digits

    def convert(self, cobol_str):
        if len(cobol_str) == 0:
            return 0
        if cobol_str[-1] in '+-':
            sign = 1 if cobol_str[-1] == '+' else -1
            numeric_part = cobol_str[:-1]
        else:
            sign = 1  # Default to positive if no sign is explicitly given
            numeric_part = cobol_str
        
        numeric_part = numeric_part.lstrip('0') or '0'

        if len(numeric_part) <= self.dec_digits:
            numeric_part = '0.' + '0' * (self.dec_digits - len(numeric_part)) + numeric_part
        else:
            numeric_part = numeric_part[:-self.dec_digits] + '.' + numeric_part[-self.dec_digits:]

        formatted_value = sign * float(numeric_part)
        return format(formatted_value, f'.{self.dec_digits}f')



class CustomUSFederalHolidayCalendar(pd.tseries.holiday.AbstractHolidayCalendar):
    rules = [
        pd.tseries.holiday.Holiday('New Years Day', month=1, day=1),
        pd.tseries.holiday.USMartinLutherKingJr,
        pd.tseries.holiday.USPresidentsDay,
        pd.tseries.holiday.USMemorialDay,
        pd.tseries.holiday.Holiday('Juneteenth Day', month=6, day=19),
        pd.tseries.holiday.Holiday('Independence Day', month=7, day=4),
        pd.tseries.holiday.USLaborDay,
        pd.tseries.holiday.USColumbusDay,
        pd.tseries.holiday.Holiday('Veterans Day', month=11, day=11),
        pd.tseries.holiday.USThanksgivingDay,
        pd.tseries.holiday.Holiday('Christmas', month=12, day=25)
    ]



class amazon():
    @staticmethod
    def get_secret(secret_name, region_name):
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager',region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e
    
        password = get_secret_value_response['SecretString']
        return password    
    
    @staticmethod
    def check_holiday(date_obj, which ='NYSE_Holiday'):
        try:
            date_obj = date_obj.date()
        except:
            date_obj = date_obj
        
        current_year = date_obj.year
        start_date = pd.to_datetime(f'{current_year}-01-01')
        end_date = pd.to_datetime(f'{current_year}-12-31')
        
        nyse = mcal.get_calendar('NYSE')
        nyse_holidays = pd.DataFrame(nyse.holidays().holidays).rename(columns={0:'Date'})
        nyse_holidays = nyse_holidays[nyse_holidays['Date'].dt.year == current_year].reset_index(drop=True)
        
        fed_holidays_calendar = CustomUSFederalHolidayCalendar()
        bank_holidays = fed_holidays_calendar.holidays(start=start_date, end=end_date)
        bank_holidays = pd.DataFrame(bank_holidays).rename(columns={0:'Date'})
        nyse_holidays['Date'] = nyse_holidays['Date'].apply(lambda x: x.date())
        bank_holidays['Date'] = bank_holidays['Date'].apply(lambda x: x.date())
    
        if which == 'NYSE_Holiday':
            if date_obj in nyse_holidays['Date'].values:
                return True
            else:
                return False
        elif which == 'Bank_Holiday':
            if date_obj in bank_holidays['Date'].values:
                return True
            else:
                return False
        
    @staticmethod
    def data_pull(sql_query, con, indicator):
        data = wr.redshift.read_sql_query(
            sql=sql_query,
            con=con
        )

        print(indicator)
        return data
    
    @staticmethod
    def sql_execute(sql_query, con, indicator):
        cursor: redshift_connector.Cursor = con.cursor()
        cursor.execute(sql_query)
        
        print(indicator)     

    @staticmethod
    def insert_table(db_params, data, con, method, mode, dtype, schema = None, table=None):
        if schema is None:
            schema = db_params['schema_name']
        if table is None:
            table=db_params['table_name']
        if method == 'copy':
            wr.redshift.copy(
                df = data,
                path =f's3://tradeup-it/parquet/{schema}/{table}',
                schema=schema,
                table=table,
                con=con,
                mode=mode, #  Append, overwrite or upsert
                use_column_names = True,
                index=False,
                dtype=dtype # Optional: specify column data types
            )
            print(f'insert: 1')
        elif method == 'to_sql':
            wr.redshift.to_sql(
                df = data,
                schema=schema,
                table=table,
                con=con,
                mode=mode, #  Append, overwrite or upsert
                use_column_names = True,
                index=False # Typically, you don't want DataFrame indexes in your database table
                #dtype={"column1": "INTEGER", "column2": "VARCHAR(255)"} # Optional: specify column data types
            )             
            print('insert: 1')   