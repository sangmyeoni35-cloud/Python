from Account.account import Account

class AccountDAO:
    def __init__(self):       #    키         값        딕셔너리인데 키에 계좌번호, 값에 객체 자체(계좌)를 저장하는 구조
        self.__accountDB = {} # 계좌번호 : account 객체

    def insert_account(self, account):  # 계좌 생성
        account_no = account.get_account_no()
        if account_no not in self.__accountDB:
            self.__accountDB[account.get_account_no()] = account
            return True
        return False

    def select_account_by_account_no(self, account_no): # 계좌 조회
        if account_no in self.__accountDB:
            return self.__accountDB[account_no] # 계좌번호에 대응하는 값(객체, 계좌) 조회
        return None

    def select_accounts_by_member_id(self, member_id): # 회원 별 계좌 조회
        account_list = []
        for account in self.__accountDB.values(): # 저장된 계좌중에서 해당 id와 같은 명의의 계좌들을 조회
            if account.get_owner() == member_id:
                account_list.append(account)
        
        if len(account_list): return account_list
        return None

    def select_all_accounts(self):  # 계좌목록
        account_list = list(self.__accountDB.values())
        if len(account_list):
            return account_list
        return None

    def update_account(self, account_no, account): # 계좌 수정
        if account_no in self.__accountDB:
            self.__accountDB[account_no] = account # 해당 계좌번호의 계좌를 바꿈
            return True
        return False
    
    def delete_account(self, account_no): # 계좌 삭제
        if account_no in self.__accountDB:
            self.__accountDB.pop(account_no) # 해당 계봐번호의 계좌를 버림
            return True
        return False

# if __name__ == '__main__':
#     dao = AccountDAO()
    
#     ac_list = dao.select_all_accounts()
#     print(ac_list)
    
#     dao.insert_account(Account('111111', 'asdf', 10000, '1234'))
#     dao.insert_account(Account('111112', 'fdsa', 20000, '1234'))
#     dao.insert_account(Account('111113', 'gerh', 43000, '1234'))
    
#     for account in dao.select_all_accounts():
#         print(account)
    
#     print(dao.select_account_by_account_no('111116'))
    
#     for account in dao.select_accounts_by_member_id('asdf'):
#         print(account)
#     print()
    
#     print(dao.select_account_by_account_no('111112'))
#     dao.update_account('111112', Account('111112', 'qwrtysd', 123458, '53213'))
#     print(dao.select_account_by_account_no('111112'))
#     print()

#     dao.delete_account('111112')
#     print(dao.select_account_by_account_no('111112'))