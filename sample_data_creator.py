import numpy as np
import pandas as pd
import namegenerator
from datetime import date, datetime, timedelta
import sqlalchemy as db

# function to create a new user
def create_user():
    name = namegenerator.gen()
    possible_plz = [69115, 69117, 69118, 69120, 69121, 69123, 69124, 69126]
    plz = np.random.choice(possible_plz)

    # create random sample signup date with an exponential growth trend to today
    y = int(np.around(np.random.exponential(2)))
    m = int(np.around(np.random.exponential(5)))
    if m > 11: m = 11 
    d = np.random.randint(1,28)

    sign_up = date(2020-y, 12-m, d).isoformat()
    
    # for a small portion of users (estimating a monthly retention of 99%) create a canellation date
    date1 = date.fromisoformat(sign_up)
    final_date = date(2020, 12, 29)
    month = timedelta(weeks=4)
    active_months = 0

    while(date1 <= final_date):
        date1 = date1 + month
        active_months += 1 
        leave = (.99 <= np.random.random_sample())
        cancellation = None
        if leave == True:
            cancellation = date1.isoformat()
            break 

    user_data = [name, plz, 1, sign_up, cancellation]
    return user_data

# create_user()

def create_claims(user_data, user_id):
    claims = []
    claim_information = ['Phone', 'Car', 'Home', 'Bike', 'X']

    start_date = date.fromisoformat(user_data[3])
    if user_data[4] == None:
        end_date = date(2020, 12, 25)
    else: end_date = date.fromisoformat(user_data[4])
    week = timedelta(weeks = 1)

    while start_date <= end_date:
        incident = np.random.choice(claim_information, p=[0.01, 0.001, 0.02, 0.01, 0.959])
        value = 0
        if incident == 'Phone': value = np.random.normal(100.0, 20.0)
        elif incident == 'Car': value = np.random.normal(1000.0, 100.0)
        elif incident == 'Home': value = np.random.normal(50.0, 10.0)
        elif incident == 'Bike': value = np.random.normal(250.0, 50.0)

        if value > 0:
            claims.append([user_id, incident, int(value), start_date])

        start_date = start_date + week

    return claims


# Populate dataframes with random sample data
user_number = 1000
users = pd.DataFrame(columns = ['name', 'plz', 'multiplier', 'sign_up', 'cancelled'])
claims = pd.DataFrame(columns = ['user_id', 'information', 'claim_height', 'date'])

for i in range(user_number):
    new_user = create_user()
    pd_new_user = pd.Series(new_user, index = users.columns)
    users = users.append(pd_new_user, ignore_index = True)

    new_claim = create_claims(new_user, i)
    pd_claim = pd.DataFrame(new_claim, columns = claims.columns)
    claims = claims.append(pd_claim, ignore_index=True)

print(users)
print(claims)

# Connect to db and write generated data to tables
# specify database configurations
config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'tim',
            'password': '13-erTuer',
            'database': 'getsafe_db'
         }

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')
# specify connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# connect to database
engine = db.create_engine(connection_str)
connection = engine.connect()

entry_users = users.to_sql('users', connection, if_exists='append', index=False)
entry_claims = claims.to_sql('claims', connection, if_exists='append', index=False)


