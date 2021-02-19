import sqlalchemy as db
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

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

# plot user number statistics
def plot_user_numbers():
    sign_ups = pd.read_sql("SELECT sign_up FROM users", connection)
    sign_outs = pd.read_sql("SELECT cancelled FROM users WHERE cancelled IS NOT NULL", connection)

    sign_ups['user_growth'] = 1
    sign_outs['user_growth'] = -1
    
    sign_ups.rename(columns={'sign_up' : 'dates'}, inplace=True)
    sign_outs.rename(columns={'cancelled' : 'dates'}, inplace=True)
    
    print(sign_ups)
    print(sign_outs)

    user_change = [sign_ups, sign_outs]

    user_change = pd.concat(user_change)
    user_change = user_change.sort_values(by='dates')
    user_change = user_change.reset_index(drop=True)
    print(user_change)

    compound = []

    for i in range(len(user_change.index)):
        compound.append(user_change['user_growth'].iloc[:i+1].sum())

    user_change['compounds'] = compound

    print(user_change)

    fig, comp = plt.subplots()
    comp.set_title('User numbers over time')
    comp.set_ylabel('Users')
    comp = sns.lineplot(x = 'dates', y = 'compounds', data = user_change) 
    change = comp.twinx()
    change.set_ylabel('change in users')
    change = sns.barplot(x='dates', y='user_growth', data = user_change)
    plt.savefig('user_numbers.png')

plot_user_numbers()
