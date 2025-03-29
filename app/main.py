from database.database import init_db
from models.user import User
from database.database import engine
from services.crud.user import usercrud, IssufisientFunds
from services.crud.historyofpaymentscrud import historyofpaymentscrud

if __name__=='__main__':
    init_db()
    
    user_functions = usercrud(engine)
    hop_functions = historyofpaymentscrud(user_functions, engine)

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
    
    
    