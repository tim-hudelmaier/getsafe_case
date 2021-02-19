import sqlalchemy as db
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from datetime import date, datetime, timedelta

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
    
    # print(sign_ups)
    # print(sign_outs)

    user_change = [sign_ups, sign_outs]

    user_change = pd.concat(user_change)
    user_change = user_change.sort_values(by='dates')
    user_change = user_change.reset_index(drop=True)
    # print(user_change)

    compound = []

    for i in range(len(user_change.index)):
        compound.append(user_change['user_growth'].iloc[:i+1].sum())

    user_change['compounds'] = compound

    # print(user_change)

   
    sns.lineplot(x = 'dates', y = 'compounds', data = user_change) 
    plt.savefig('user_numbers.png')

# plot_user_numbers()

def plot_user_revenue(user_id):
    user_data = pd.read_sql("SELECT * FROM users WHERE user_id = %s ;" % user_id, connection)
    user_claims = pd.read_sql("SELECT * FROM claims WHERE user_id = %s AND information IN (SELECT pol_name FROM policies WHERE pol_id IN (SELECT pol_id FROM user_groups WHERE user_id = %s));" % (user_id, user_id), connection)
    user_policies = pd.read_sql("SELECT * FROM policies WHERE pol_id IN (SELECT pol_id FROM user_groups WHERE user_id = %s);" % user_id,connection)

    # clean claims from too high claims
    for index, row in user_claims.iterrows():
        if row['claim_height'] > user_policies['max_claim'].loc[user_policies[user_policies['pol_name']==row['information']].index.values].iloc[0]:
            user_claims.drop(index)

    print(user_data)

    day = timedelta(days = 1)
    sign_up_d = user_data['sign_up']
    if user_data['cancelled'].iloc[0] != None:
        end_d = user_data['sign_up']
    else: end_d = date.today()

    revenue_data = []
    comp_returns = 0

    days = timedelta(days = 0)
    month = timedelta(days = 30)
    print(sign_up_d.iloc[0])
    # print(end_d)
    print(user_claims)
    su = date().fromisoformat(str(sign_up_d.iloc[0]))
    while su <= end_d:
        if days < month:
            days += day
        else:
            comp_returns += user_policies['cost_per_month'].sum()
            revenue_data.append([sign_up_d.iloc[0], comp_returns])
            days = timedelta(days = 0)
        # print(user_claims.date.values.tolist())
        # print(type(user_claims.date.values.tolist()[0]))
        # print(sign_up_d.iloc[0])
        # print(type(sign_up_d.iloc[0]))
        # print(user_claims['claim_height'])
        # user_claims.set_index('date', inplace=True)
        
        # print(user_claims)
        # sign_up_d.iloc[0] = date(2018, 7, 5)

        if su == user_claims.date.values.tolist()[0]:
            print('works!')
            # revenue_data.append([sign_up_d.iloc[0], comp_returns])
        
        su = su + day

    compound_returns = pd.DataFrame(revenue_data, columns=['date', 'compounded returns'])

    # print(compound_returns)

    sns.lineplot(x = 'date', y = 'compounded returns', data = compound_returns)
    plt.savefig('comp_returns_on_user_%s.png' % user_id)


plot_user_revenue(332)

