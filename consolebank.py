from Member.member import Member
from Member.member_service import MemberService
from Member.member_dao import MemberDAO
from Account.account import Account
from Account.account_service import AccountService
from Account.account_dao import AccountDAO

class ConsoleBank:
    start_menu = ['종료', '로그인', '회원가입'] # 시작 메뉴
    banking_menu = ['로그아웃', '계좌목록', '입금', '출금', '계좌생성', '계좌해지', '내 정보'] # 회원 메뉴
    member_myinfo_menu = ['돌아가기', '내 정보 조회', '비밀번호 수정', '회원탈퇴'] # 내 정보 매뉴
    admin_menu = ['로그아웃', '회원관리', '계좌관리'] # 관리자 메뉴
    admin_account_menu = ['돌아가기', '전체계좌목록', '회원별계좌목록'] # 계좌관리 메뉴
    admin_member_menu = ['돌아가기', '회원목록', '회원정보조회', '회원강퇴'] # 회원관리 메뉴
    balance_confirm = ['아니요', '예']

    def __init__(self):
        self.msv = MemberService(MemberDAO()) # 멤버서비스
        self.asv = AccountService(AccountDAO()) # 어카운트서비스
        # # for test
        # self.msv.join(Member(0, 'A', '1111', 'aaaa'))
        # self.asv.create_account(Account(0, 'Q', 10000, '0000'))

    def main(self): # 메인
        self.show_welcome() # ==== Console Bank ====
        self.run_start_menu() # 시작메뉴 보여주기
        self.say_goodbye() # ==== Bye ====
#-----------------------------------------------------------------------
    def show_welcome(self): # ==== Console Bank ====
        print('=' * 50)
        title = 'Console Bank'
        print(f'{title:^50}')
        print('=' * 50)
        
    def say_goodbye(self): # ==== Bye ====
        print('>> Console Bank 를 이용해 주셔서 감사합니다.')

    def select_menu(self, menu_list): # 메뉴 선택( 번호 반환 )
        print('-'*50)
        for index in range(1, len(menu_list)):
            print(f'{index}. {menu_list[index]}')
        print(f'0. {menu_list[0]}')
        print('-'*50)
        try:
            num = int(input('>> 메뉴 : '))
        except ValueError:
            return -1
        else:
            return num
#-----------------------------------------------------------------------    
    def run_start_menu(self): # 시작 메뉴 보여주기
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)
            if menu == 0: break # 종료
            elif menu == 1:
                self.menu_login() # 로그인
            elif menu == 2:
                self.menu_join() # 회원가입
            else:
                print('없는 메뉴입니다.')

    def menu_join(self): # 시작 메뉴 > 회원가입
        print('>>>>> 회원가입 <<<<<')
        id = input('아이디 입력 : ')
        password = input('패스워드 입력 : ')
        name = input('이름 입력 : ')
        if self.msv.join(Member(None, id, password, name)):
            print('회원가입에 성공하였습니다.')
        else:
            print('회원가입에 실패하였습니다.')

    def menu_login(self): # 시작 메뉴 > 로그인
        print('>>>>> 로그인 <<<<<')
        id = input('아이디 입력 : ')
        password = input('패스워드 입력 : ')
        if self.msv.login(id, password):
            print(f'{self.msv.current_user.get_name()}님, 환영합니다.')
            if self.msv.current_user == MemberService.ADMIN_ID:
                self.run_admin_menu()
            else:
                self.run_banking_menu()
        else:
            print('로그인에 실패하였습니다.')

    def menu_logout(self): # 모든 메뉴 공통 > 로그아웃
        self.msv.logout()
#-----------------------------------------------------------------------
    def run_banking_menu(self): # 회원 메뉴 보여주기
        print('>>>>> 회원 메뉴 <<<<<')
        while True:
            menu = self.select_menu(ConsoleBank.banking_menu)
            if menu == 0: 
                self.msv.logout() # 로그아웃
                break
            elif menu == 1:
                self.menu_list_my_accounts() # 계좌목록
            elif menu == 2:
                self.menu_deposit() # 입금
            elif menu == 3:
                self.menu_withdraw() # 출금
            elif menu == 4:
                self.menu_create_account() # 계좌생성
            elif menu == 5:
                self.menu_delete_account() # 계좌해지
            elif menu == 6:
                self.menu_myinfo() # 내 정보
            else:
                print('없는 메뉴입니다.')

    def menu_list_my_accounts(self): # 회원 메뉴 > 계좌목록
        print('>>>>> 내 계좌 목록 <<<<<')
        self.list_members_accounts(self.msv.current_user)

    def list_members_accounts(self, id): # ( 아이디에 대응하는 계좌 정보 리스트로 출력 ) 공통
        account_list = self.asv.get_members_accounts(id)
        print('-'*50)
        if account_list:
            for account in account_list:
                print(account)
        else:
            print('등록된 계좌가 없습니다.')
        print('-'*50)

    def menu_deposit(self): # 회원 메뉴 > 입금
        print('>>>>> 입금 <<<<<')
        self.list_members_accounts(self.msv.current_user)
        account_no = input('대상 계좌번호 : ')
        amount = int(input('입금액 : '))
        if self.asv.deposit(account_no, amount):
            print(f'대상 계좌 >> {account_no}, {amount}원을 입금했습니다.')
            balance = self.asv.get_account_balance(account_no)
            if balance >= 0:
                print(f'해당계좌 현재 잔액 : {balance:,}')
        else:
            print('입금을 할 수 없습니다.')

    def menu_withdraw(self): # 회원 메뉴 > 출금
        print('>>>>> 출금 <<<<<')
        id = input('아이디 입력 : ')
        password = input('패스워드 입력 : ')
        if id == self.msv.current_user:
            if password == self.msv.view_member_info(id).get_password():
                print('인증에 성공하였습니다.')
                self.list_members_accounts(self.msv.current_user)
                account_no = input('대상 계좌번호 : ')
                amount = int(input('출금액 : '))
                if self.asv.withdraw(id, account_no, amount, password):
                    print(f'대상 계좌 >> {account_no}, {amount}원을 출금했습니다.')
                    balance = self.asv.get_account_balance(account_no)
                    if balance >= 0:
                        print(f'해당계좌 현재 잔액 : {balance:,}')
                else:
                    print('출금을 할 수 없습니다.')
        else:
            print('회원 정보가 일치하지 않습니다.')
        

    def menu_create_account(self): # 회원 메뉴 > 계좌 생성
        id = input('아이디 입력 : ')
        password = input('패스워드 입력 : ')
        if self.asv.create_account(None, id, password):
            print('계좌생성이 완료되었습니다.')
        else:
            print('계좌생성에 실패하였습니다.')

    def remain_balance(self, id): # 해당 계정에 잔액이 남았는지 확인 ( 공통 ) / 회원 > 해지, 탈퇴 / 관리자 > 강퇴
        accounts = self.asv.get_members_accounts(id)
        balance = 0
        for account in accounts:
            balance += account.get_balance()
        if balance == 0:
            return False
        else:
            return True

    def menu_delete_account(self): # 회원 메뉴 > 계좌 해지
        account_no = input('해지할 계좌번호 입력 : ')
        id = input('아이디 입력 : ')
        password = input('패스워드 입력 : ')
        if self.remain_balance(self.msv.current_user):
            menu = self.run_balance_menu()
            if menu == 0:
                return
            elif menu == 1:
                if self.asv.delete_account(id, account_no, password):
                    print('해당 계좌가 해지되었습니다.')
                else:
                    print('해지에 실패하였습니다.')
        else:
            if self.asv.delete_account(id, account_no, password):
                    print('해당 계좌가 해지되었습니다.')
            else:
                print('해지에 실패하였습니다.')

    def run_balance_menu(self):
        print('해당 회원 계정의 1개 이상 계좌에 잔액이 남아있습니다')
        print('탈퇴 하시겠습니까?')
        menu = self.select_menu(ConsoleBank.balance_confirm)
        return menu

    def menu_myinfo(self): # 회원 메뉴 > 내 정보
        self.run_my_info_menu()
#-----------------------------------------------------------------------
    def run_my_info_menu(self): # 내 정보 메뉴 보여주기
        print('>>>>> 내 정보 메뉴 <<<<<')
        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0: 
                break
            elif menu == 1:
                self.menu_view_myinfo()
            elif menu == 2:
                self.menu_update_password()
            elif menu == 3:
                self.menu_delete_membership()
            else:
                print('없는 메뉴입니다.')

    def menu_view_myinfo(self): # 내 정보 메뉴 > 내 정보 조회
        self.msv.view_member_info(self.msv.current_user)

    def menu_update_password(self): # 내 정보 메뉴 > 비밀번호 수정
        org_password = input('기존 패스워드 입력 : ')
        new_password = input('새 패스워드 입력 : ')
        if self.msv.update_member_password(self.msv.current_user, org_password, new_password):
            print('패스워드가 변경되었습니다.')
        else:
            print('패스워드 변경에 실패하였습니다.')

    def menu_delete_membership(self): # 내 정보 메뉴 > 회원탈퇴
        password = input('패스워드 입력 : ')
        if self.remain_balance(self.msv.current_user):
            menu = self.run_balance_menu()
            if menu == 0:
                print('탈퇴를 취소하였습니다.')
                return
            elif menu == 1:
                if password == self.msv.view_member_info(self.msv.current_user).get_password():
                    self.msv.remove_member(self.msv.current_user)
                    self.msv.logout()
        else:
            if password == self.msv.view_member_info(self.msv.current_user).get_password():
                self.msv.remove_member(self.msv.current_user)
                self.msv.logout()
#-----------------------------------------------------------------------
    def run_admin_menu(self): # 관리자 메뉴 보여주기
        while True:
            menu = self.select_menu(ConsoleBank.admin_menu)
            if menu == 0: 
                self.msv.logout() # 로그아웃
                break
            elif menu == 1:
                self.menu_manage_members() # 회원관리
            elif menu == 2:
                self.menu_manage_accounts() # 계좌관리
            else:
                print('없는 메뉴입니다.')

    def menu_manage_members(self): # 관리자 메뉴 > 회원관리
        self.run_admin_member_menu()

    def menu_manage_accounts(self): # 관리자 메뉴 > 계좌관리
        self.run_admin_account_menu()
#-----------------------------------------------------------------------
    def run_admin_account_menu(self): # ( 관리자 )계좌관리 메뉴 보여주기
        while True:
            menu = self.select_menu(ConsoleBank.admin_account_menu)
            if menu == 0: 
                break # 돌아가기
            elif menu == 1:
                self.menu_list_all_accounts() # 전체 계좌목록
            elif menu == 2:
                self.menu_list_member_accounts() # 회원 별 계좌목록
            else:
                print('없는 메뉴입니다.')

    def menu_list_all_accounts(self): # 계좌관리 메뉴 > 전체 계좌목록
        if self.asv.get_all_accounts():
            print()
        else:
            print('현재 등록된 계좌가 없습니다.')

    def menu_list_member_accounts(self): # 계좌관리 메뉴 > 회원 별 계좌목록
        id = input('회원 아이디 입력 : ')
        if self.list_members_accounts(id):
            print()
        else:
            print('존재하지 않는 회원입니다.')
#-----------------------------------------------------------------------
    def run_admin_member_menu(self): # ( 관리자 )회원관리 메뉴 보여주기
        while True:
            menu = self.select_menu(ConsoleBank.admin_member_menu)
            if menu == 0: 
                break # 돌아가기
            elif menu == 1:
                self.menu_list_members() # 회원목록
            elif menu == 2:
                self.menu_view_member_info() # 회원 정보 조회
            elif menu == 3:
                self.menu_delete_member() # 회원 강퇴(탈퇴)
            else:
                print('없는 메뉴입니다.')

    def menu_list_members(self): # 회원관리 메뉴 > 회원목록
        member_list = self.msv.list_members()
        if member_list:
            for info in member_list:
                print(f'{info.get_member_no()}\t{info.get_id()}\t{info.get_name()}')

    def menu_view_member_info(self): # 회원관리 메뉴 > 회원 정보 조회
        id = input('회원 아이디 입력 : ')
        if self.msv.view_member_info(id):
            print()
        else:
            print('존재하지 않는 회원입니다.')

    def menu_delete_member(self): # 회원관리 메뉴 > 회원 강퇴(탈퇴)
        id = input('회원 아이디 입력 : ')
        if self.remain_balance(id):
            print('해당 회원의 1개 이상 계좌에 잔액이 남아있습니다.')
            return
        else:
            if self.msv.remove_member(id):
                print('회원이 탈퇴되었습니다.')
            else:
                print('존재하지 않는 회원입니다.')



if __name__ == '__main__':
    app = ConsoleBank()
    app.main()