from database.database import init_db
from models.user import User
from models.paymenthistory import PaymentHistory
from models.taskshistory import TasksHistory

from schemas.user import SUser
from schemas.paymenthistory import SPaymentHistory
from schemas.taskshistory import STasksHistory
from services.crud.usercrud import UsersCRUD
from services.crud.paymenthistorycrud import PaymentHistoryCRUD
from services.crud.taskshistorycrud import TasksHistoryCRUD
from services.crud.exceptions import InsufficientFunds

from random import randint

if __name__=='__main__':
    init_db()

    u1 = SUser(email=f'user_main@mydb.one', 
                      first_name=f'User_main', 
                      last_name=f'Fortest_main', 
                      password=f'pw_main', 
                      balance=300.0, 
                      is_admin=True,
                      loyalty=1.0)
    UsersCRUD.add(u1)

    users = UsersCRUD.find_all_users()
    UsersCRUD.allow_admin_by_id(users[0].id)
    UsersCRUD.disallow_admin_by_email(users[0].email)
    

    payments = [1.0 * randint(1, 100) for idx in range(len(users))]
    spends = [-1.0 * randint(1, 100) for idx in range(len(users))]

    for idx, user_item in enumerate(users):
        balance = UsersCRUD.get_balance_by_id(user_item.id)
        ph = SPaymentHistory(user_id=user_item.id, 
                            value=payments[idx],
                            value_before=balance,
                            value_after=balance+payments[idx],
                            status='pending')
        pay_item = PaymentHistoryCRUD.add(ph)
        UsersCRUD.add_payment_by_id(user_item.id, payments[idx])
        PaymentHistoryCRUD.update_status_by_id(pay_item.id, 'complete')

    for idx, user_item in enumerate(users):
        balance = UsersCRUD.get_balance_by_id(user_item.id)
        ph = SPaymentHistory(user_id=user_item.id, 
                            value=spends[idx],
                            value_before=balance,
                            value_after=balance+spends[idx],
                            status='pending')
        try:
            pay_item = PaymentHistoryCRUD.add(ph)
            UsersCRUD.spend_payment_by_id(user_item.id, spends[idx])
            PaymentHistoryCRUD.update_status_by_id(pay_item.id, 'complete')

        except InsufficientFunds:
            PaymentHistoryCRUD.update_status_by_id(pay_item.id, 'rejected')
            print(f'У пользователя {user_item} недостаточно средств для {spends[idx]} на балансе {user_item.balance}')

    for pay_item in PaymentHistoryCRUD.find_all_by_user(users[0]):
        print(f'id={pay_item.id}, ' 
              f'from={pay_item.value_before}, '
              f'to={pay_item.value_after}, '
              f'with={pay_item.value} '
              f'status={pay_item.status}, '
              f'date={pay_item.processed}')
        
    for idx, user_item in enumerate(users):
        th = STasksHistory(user_id=user_item.id, 
                            image='./ocr_in_image.png',
                            status='complete',
                            result='',
                            cost=30.0)
        TasksHistoryCRUD.add(th)

        

    