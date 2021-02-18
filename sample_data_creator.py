import numpy as np
import pandas as pd
import namegenerator
from datetime import date, datetime, timedelta


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
    final_date = date(2020, 12, 25)
    month = timedelta(weeks=4)
    active_months = 0

    while(date1 <= final_date):
        date1 = date1 + month
        active_months += 1 
        leave = (.99 <= np.random.random_sample())
        if leave == True:
            cancellation = date1.isoformat()
            break
        else:
            cancellation = '' 

    user_data = [name, plz, 1, sign_up, cancellation]
    return user_data

create_user()
