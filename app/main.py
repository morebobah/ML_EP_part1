from database.database import init_db
from models.user import User
from models.historyofpayments import Historyofpayments
from models.historyoftasks import Historyoftasks
from database.database import engine
from services.crud.user import usercrud, IssufisientFunds
from services.crud.mlmodel import mlmodelcrud
from services.crud.historyofpaymentscrud import historyofpaymentscrud
from services.crud.historyofmlmodelscrud import historyofmlmodelscrud

if __name__=='__main__':
    init_db()
    
    user_functions = usercrud(engine)
    hop_functions = historyofpaymentscrud(engine)
    ml_functions = mlmodelcrud(engine)
    hot_functions = historyofmlmodelscrud(engine)

    user_functions.register(hop_functions)
    ml_functions.register(hot_functions)
    ml_functions.register(user_functions)

    ml_functions.cost_per_result = 50.0

    users = user_functions.get_all_users()

    
    print(f'Balance of user {users[1]} is {user_functions.get_balance(users[1])} credits.')
    user_functions.add_payment(users[1], 100)
    print(f'Balance of user {users[1]} is {user_functions.get_balance(users[1])} credits.')
    user_functions.add_payment(users[1], 100)
    user_functions.add_payment(users[1], 100)
    user_functions.add_payment(users[1], 100)
    
    for user_item in users:
        user_functions.add_payment(user_item, 50)

    try:
        user_functions.spend_payment(users[3], -60)
    except IssufisientFunds:
        print(f'Issufisient funds')

    print(f'Balance of user {users[1]} is {user_functions.get_balance(users[1])} credits.')
    user_functions.spend_payment(users[1], -30)
    print(f'Balance of user {users[1]} is {user_functions.get_balance(users[1])} credits.')
    
    print(f'Table of payments for user {users[1]}')
    for item in hop_functions.get_events({'user_id': users[1].id}):
        print(f'{item}')

    print(f'Balance of user {users[1]} is {user_functions.get_balance(users[1])} credits.')

    mltasks = []
    mltasks.append(Historyoftasks(user=users[1],
                                 image='./static/acff34-4151fa-img.png'))
    mltasks.append(Historyoftasks(user=users[2],
                                 image='./static/acff34-4151fa-img.png'))
    for ml_item in mltasks:
        ml_functions.do_result(ml_item)

    
    print(f'Balance of user {users[1]} is {user_functions.get_balance(users[1])} credits.')
    print(f'Balance of user {users[2]} is {user_functions.get_balance(users[1])} credits.')
    
    print(f'Table of payments for user {users[1]}')
    for item in hop_functions.get_events({'user_id': users[1].id}):
        print(f'{item}')
    

    print(f'Table of tasks for user {users[1]}')
    for item in hot_functions.get_events({'user_id': users[1].id}):
        print(f'{item}')