from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Account.account import Account
from Account.account_dao import AccountDAO
from Account.account_service import AccountService

class ConsoleBank:
    start_menu = ['종료', '로그인', '로그아웃', '회원가입']
    banking_mene = ['로그아웃', '계좌목록', '입금', '출금', '계좌생성', '계좌해지', '내정보']
    member_myinfo_menu = ['돌아가기', '비밀번호', '내정보']
    admin_menu = ['로그아웃', '회원관리', '계좌관리']
    admin_account_menu = ['돌아가기', '전체계좌목록', '회원별계좌목록']
    admin_member_menu = ['돌아가기', '회원목록', '회원정보조회', '회원강퇴']

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.asv = AccountService(AccountDA())
        # for test
        self.msv.join(Member('sangmyeoni', '1234', '이상면'))
        self.asv.create_account(Account(0, 'sangmyeoni', 10000, '1111'))

    def main(self):
        self.show_welcom()
        self.run_start_menu()
        self.say_goodbye()
       
    def show_welcom(self):
        print('============= sangmyeoni Console Bank ============')

    def say_goodbye(self):
        print('>> sangmyeoni Console Bank를 이용해 주셔서 감사합니다.')

    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)
            if menu == 0: break
            elif menu == 1:
                self.menu_login()
            elif menu == 2:
                self.menu_join()

    def select_menu(self, menu_list):
        print('-------------------')
        for index in rang(1, len(menu_list)):
            print(f'{index}. {menu_list[index]}')
        print(f'0. {menu_lis[0]}')
        print('------------------------------------')
        try:
            num = int(input('>>메뉴 : '))
        except ValueError:
            return -1
        else:
            return num

    def menu_login(self):
        print('>>>>>>> 로그인 <<<<<<<<<')
        if self.msv.login('sangmyeoni', '1234'):
            print(f'{self.msv.viw_member_info(self.msv.current_user).get_name()}님 환영합니다.')
            if self.msv.current_user == MemberServic.ADMIN_ID:
                self.run_admin_menu()
            else:
                self.run_banking_menu()
        else:
            print('로그인을 할 수 없습니다.') 

    def menu_logout(self):
        print('>>>>>> 회원가입 <<<<<<<<') 
        if self.msv.join(Member('sangmyeoni', '1234', '이상면')):
            prnt('회원가입에 성공하였습니다.')
        else:
            print('회원가입을 할 수 없습니다.')

def run_banking_menu(self):
    print('>>>>> 은행 업무 메뉴 <<<<<<<')
    while True:
    menu = self.select_menu(self.banking_menu)
    if menu == 0:
        self.msv.logout()
        break
    elif menu == 1:
        self.menu_list_my_accounts()
    elif menu == 2:
        self.menu_deposit()
    elif menu == 3:
        self.menu_withdraw()
    elif menu == 4:
        self.menu_create_account()
    elif menu == 5:
        self.menu_delete_account()
    elif menu == 6:
        self.menu_myinfo()

def menu_list_my_accounts():
    print('>>>>> 내 계좌 목록 <<<<<<')
    self.list_members_accounts(self.msv.current_user)

def list_members_accounts(self, id):
    account_list = self.asv.get_members_accounts(id)
    print('------------------------------------')
    if account_list:
        for account in account_list:
            print(account)
    else:
        print('등록된 계좌가 없습니다.')
    print('------------------------------------')

def menu_deposit(self):
    print('>>>>> 입금 <<<<<')
    self.list_members_accounts(self.msv.current_user)
    account_no = input('>> 계좌번호 : ')
    amount = int(input('>> 입금액 :  '))
    if self.asv.deposit(account_no, amount):
        print(f'계좌번호 {account_no}에 {amount: ,}원을 입금했습니다.')
        balance = self.asv.get_accoun_balance(account_no)
        if balance >= 0:
            print(f'잔액 : {balance: ,}')
    else:
        print('입금을 할 수 없습니다.')

def menu_withdraw(self):
    print('>>>>>> 출금 <<<<<<<<')
    self.list_members_accounts(self.msv.current_user) 
    account_no = input('>> 계좌번호 : ')
    amount = int(input('>> 출금액 : '))
    password = input('>> 비밀번호 : ')
    try:
        self.asv.withdraw(self.msv.current_user, account_no, amount, password)
    except ValueError:
        print(f'잔액이 부족합니다. -> 현재 잔액 : {self.asv.get_account_balance(account_no):,}')
    except LookupError:
        print('없는 계좌번호입니다.')
    except KeyError:
        print('출금을 할 수 없습니다.')
    else:
        print(f'계좌번호 {account_no}에서 {amount:,}원을 출금했습니다.')
        balance= self.asv.get_account_balance(account_no)
        print(f'잔액 : {balance:,}')

def menu_create_account(self):
    print('>>>>>> 계좌생성 <<<<<<<')
    password = input('비밀번호 : ')
    balance = int(input('>> 최초 입금액: '))
    if self.asv.create_account(Account(0, self.msv.current_user, balance, password)):
        print('계좌를 생성하였습니다.')
        self.list_member_accounts(self.msv.current_user)
    else:
        print('계좌 생성에 실패하였습니다.')

def menu_delete_account(self):
    print('>>>> 계좌 해지 <<<<<<<')
    self.list_members_accounts(self.msv.current_user)
    account_no = input('>> 계좌번호 : ')
    password= input('>> 계좌비밀버호 : ')
    try:
        self.asv.delete_acount(self.msv.current_user, account_no, password)
    except KeyError:
        print('계좌를 해지할 수 없습니다.')
    except LookupError:
        print('없는 계좌번호입니다.')
    except ValueError:
        print(f'잔액 {self.asv.get_account_balance()}원이 있습니다. 모두 출금 후 계좌를 해지하세요.')


    # 내 정보
def menu_myinfo(self):
    self.run_my_info_menu()

def run_my_info_menu(self):
    # 각 메뉴의 동작
    while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0:
                print('회원메뉴로 돌아갑니다')
                return
            elif menu == 1:
                self.menu_view_myinfo()
            elif menu == 2:
                self.menu_update_pw()
            elif menu == 3:
                self.menu_delete_membership()

    # 내 정보 보기
def menu_view_myinfo(self):
        myinfo = self.msv.view_member_info(self.msv.current_user)
        print(myinfo)

    # 비밀번호 수정
def menu_update_pw(self):
        id = input(f'아이디: ')
        org_pw = input(f'현재 비밀번호: ')
        new_pw = input(f'새 비밀번호: ')
        print()
        member_pw = self.msv.update_member_pw(id, org_pw, new_pw)
        if member_pw == True:
            print('비밀번호가 바뀌었습니다')
        else:
            print('ERROR : 아이디나 비밀번호가 일치하지 않습니다.')

    # 회원탈퇴
def menu_delete_membership(self):
                id = input(f'아이디: ')
        print()
        delete_member = self.msv.remove_member(id)
        if delete_member == True:
            print('계정이 삭제되었습니다')
        else:
            print('ERROR : 아이디가 일치하지 않습니다.')


# admin_menu ==================================================================

def run_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_menu)
            if menu == 0:
                self.msv.logout()
                print('로그아웃되었습니다')
                return
            elif menu == 1:
                self.menu_manage_members()
            elif menu == 2:
                self.menu_manage_accounts()


def menu_manage_members(self):
        self.run_admin_member_menu()


def menu_manage_accounts(self):
    self.run_admin_account_menu()




# admin_account_menu
def run_admin_account_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_account_menu)
            if menu == 0:
                print('관리자메뉴로 돌아갑니다')
                return
            elif menu == 1:
                self.menu_list_all_accounts()
            elif menu == 2:
                self.menu_list_member_accounts()

    # 전체계좌목록
def menu_list_all_accounts(self):
        all_accounts = self.asv.get_all_accounts()
        if all_accounts:
            for accounts in all_accounts:
                print(accounts)
        else:
            print('생성된 계좌가 없습니다')

   # 회원별계좌목록
def menu_list_member_accounts(self):
        id = input(f'확인할 회원 아이디: ')
        print()
        check_member_accounts = self.asv.get_members_accounts(id)
        if check_member_accounts:
            for member_accounts in check_member_accounts:
                print(member_accounts)
        else:
            print('회원이 보유한 계좌가 없거나 존재하지 않는 회원입니다')

# admin_member_menu ==================================================================

    def run_admin_member_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_member_menu)
            if menu == 0:
                print('관리자 메뉴로 돌아갑니다')
                return
            elif menu == 1:
                self.menu_list_members()
            elif menu == 2:
                self.menu_view_member_info()
            elif menu == 3:
                self.menu_delete_member()

    # 회원목록
    def menu_list_members(self):
        list_members = self.msv.list_members()
        if list_members:
            for members in list_members:
                print(members)
        else:
            print('가입된 회원이 없습니다')

    # 회원정보조회
    def menu_view_member_info(self):
        id = input(f'확인할 회원 아이디: ')
        print()
        check_member_info = self.msv.view_member_info(id)
        print(check_member_info)

    # 회원강퇴
    def menu_delete_member(self):
        id = input(f'아이디: ')
        print()

  delete_member = self.msv.remove_member(id)
        if delete_member == True:
            print('계정이 삭제되었습니다')
        else:
            print('ERROR : 아이디가 일치하지 않습니다.')


if __name__ == '__main__':
    app = ConsoleBank()
    app.main()