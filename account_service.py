from Account.account import Account
from Account.account_dao import AccountDAO

class AccountService:
    account_no_seq = 111111 # 계좌번호 자동 생성 초기값

    def __init__(self, account_dao):
        self.__dao = account_dao
    
    def create_account(self, account): # 계좌 생성
        account.set_account_no(AccountService.account_no_seq)
        AccountService.account_no_seq += 1 # 생성후 계좌번호 자동 + 1
        return self.__dao.insert_account(account)

    def get_all_accounts(self): # 계좌 목록
        return self.__dao.select_all_accounts()

    def get_members_accounts(self, id): # 회원 별 계좌 조회
        return self.__dao.select_accounts_by_member_id(id)
    
    def get_account_balance(self, account_no):
        account = self.__dao.select_account_by_account_no(account_no)
        if account:
            return account.get_balance()
        return -1

    def deposit(self, account_no, amount): # 입금
        account = self.__dao.select_account_by_account_no(account_no)
        if account:
            new_balance = account.get_balance() + amount
            account.set_balance(new_balance)
            return self.__dao.update_account(account_no, account)
        return False

    def withdraw(self, id, account_no, amount, password): # 출금
        account = self.__dao.select_account_by_account_no(account_no)
        if account:
            if account.get_owner() != id or account.get_password() != password:
                raise KeyError
            new_balance = account.get_balance() - amount
            if new_balance < 0:
                raise ValueError
            account.set_balance(new_balance)
            return self.__dao.update_account(account_no, account)
        return False

    def delete_account(self, id, account_no, password): # 계좌 삭제
        account = self.__dao.select_account_by_account_no(account_no)
        if not account: return False
        if account.get_owner() != id or account.get_password() != password:
            raise KeyError
        return self.__dao.delete_account(account_no)

if __name__ == '__main__':
    aservice = AccountService(AccountDAO())
    aservice.create_account(Account(0, 'asdf', 10000, '1111'))
    aservice.create_account(Account(0, 'qerhdcfgn', 40000, '2222'))
    aservice.create_account(Account(0, 'fdarha', 643264, '3333'))
    for account in aservice.get_all_accounts():
        print(account)
    print()

    for account in aservice.get_members_accounts('fdarha'):
        print(account)
    print()

    if aservice.deposit(111112, 2000):
        for account in aservice.get_members_accounts('qerhdcfgn'):
            print(account)
    else: print('없는 계좌입니다.')
    print()

    try:
        aservice.withdraw('asdf', 111111, 10000, '1111')
    except Exception as e:
        print(type(e))
    else:
        for account in aservice.get_all_accounts():
            print(account)
    print()

    try:
        aservice.delete_account('fdarha', 111113, '3333')
    except Exception as e:
        print(type(e))
    else:
        if account:
            for account in aservice.get_all_accounts():
                print(account)
        else:
            print('없는 계좌입니다.')