from member import Member
from member_dao import MemberDAO
from member_service import MemberService

class MemberManager:
    start_menu = ['종료', '로그인', '회원가입']
    admin_menu = ['로그아웃', '회원목록', '회원정보조회', '회원탈퇴']
    member_menu = ['로그아웃', '내정보조회', '내정보수정', '회원탈퇴']
    member_update_menu = ['돌아가기', '아이디변경', '비밀번호변경']

    def __init__(self):
        self.ms = MemberService(MemberDAO()) # DB에 대한 의존성 주입

    def main(self):
        self.show_welcome() # ========== Member Manager ==========
        while True:
            menu = self.select_menu(MemberManager.start_menu) # 시작 메뉴
            if menu == 0: break # 종료
            elif menu == 1: # 로그인
                self.start_menu_login()
            elif menu == 2: # 회원가입
                self.start_menu_join()
            else:
                print('없는 메뉴입니다.')
        self.say_goodbye() # 안녕히가세요

    def start_menu_login(self): # 시작 메뉴 > 로그인
        id = input('>> id : ')
        password = input('>> password : ') 
        if self.ms.login(id, password):
            if self.ms.current_user == MemberService.ADMIN_ID:
                self.show_admin_menu()
            else:
                self.show_member_menu()
        else:
            print('로그인에 실패하였습니다.')

    def start_menu_join(self): # 시작 메뉴 > 회원가입
        id = input('>> id : ')
        password = input('>> password : ')
        name = input('>> name : ')
        member = Member(None, id, password, name)
        if self.ms.join(member):
            print('회원가입이 완료되었습니다.')
        else:
            print('회원가입에 실패하였습니다.')

    def show_admin_menu(self): # 관리자 메뉴 출력
        print('------------ 관리자 메뉴 ------------')
        while True:
            menu = self.select_menu(MemberManager.admin_menu)
            if menu == 0: # 로그아웃
                self.logout()
                break
            elif menu == 1: # 회원목록
                self.admin_view_list_member()
            elif menu == 2: # 회원정보조회
                self.admin_view_member_info()
            elif menu == 3: # 회원탈퇴(강퇴)
                self.admin_remove_member()
            else:
                print('없는 메뉴입니다.')

    def logout(self): # 관리자, 회원 > 공통 로그아웃
        self.ms.logout()

    def admin_view_list_member(self): # 관리자 메뉴 > 회원 목록 보기
        if self.ms.current_user != MemberService.ADMIN_ID:
            print('사용 권한이 없습니다.')
            return
        member_list = self.ms.list_members()
        if len(member_list) <= 1:
            print('가입한 회원이 없습니다.')
        else:
            for member in member_list[1:]:
                print(f'{member.get_member_no()}\t{member.get_id()}\t{member.get_name()}')

    def admin_view_member_info(self): # 관리자 메뉴 > 회원 정보 조회
        id = input('>> id : ')
        member = self.ms.view_member_info(id)
        if member:
            print(f'{member.get_member_no()}\t{member.get_id()}\t{member.get_name()}')
        else:
            print('존재하지 않는 아이디입니다.')

    def admin_remove_member(self): # 관리자 메뉴 > 회원 탈퇴(강퇴)
        id = input('>> id : ')
        if id == MemberService.ADMIN_ID:
            print('탈퇴할 수 없는 계정입니다.')
            return
        if self.ms.remove_member(id):
            print('회원탈퇴가 완료되었습니다.')
        else:
            print('회원탈퇴에 실패하였습니다.')

    def show_member_menu(self): # 회원 메뉴 출력
        print('------------- 회원 메뉴 -------------')
        while True:
            menu = self.select_menu(MemberManager.member_menu)
            if menu == 0: # 로그아웃
                self.logout()
                break
            elif menu == 1: # 내정보조회
                self.member_view_my_info()
            elif menu == 2: # 내정보수정
                self.show_member_update_menu() # 수정 메뉴 출력
            elif menu == 3: # 회원탈퇴
                self.member_remove_member()
                self.logout()
                break
            else:
                print('없는 메뉴입니다.')

    def member_view_my_info(self): # 회원 메뉴 > 내 정보 조회
        print(self.ms.view_member_info(self.ms.current_user))

    def show_member_update_menu(self): # 회원 메뉴 > 내 정보 수정(수정 메뉴 출력)
        print('------ 수정할 정보를 선택하세요 -------')
        while True:
            menu = self.select_menu(MemberManager.member_update_menu)
            if menu == 0: # 돌아가기
                break
            elif menu == 1: # 아이디변경
                self.update_my_id()
            elif menu == 2: # 패스워드변경
                self.update_my_password()
        
    def update_my_id(self): # 내 정보 수정 > 아이디 수정
        org_id = input('>> 기존 아이디 : ')
        new_id = input('>> 새 아이디 : ')
        if self.ms.update_member_id(org_id, new_id):
            print('아이디가 변경되었습니다')
        else: print('아이디 변경에 실패하였습니다')

    def update_my_password(self):
        org_password = input('기존 패스워드 : ')
        new_password = input('새 패스워드 : ')
        if self.ms.update_member_password(self.ms.current_user, org_password, new_password):
            print('패스워드가 변경되었습니다')
        else: 
            print('패스워드 변경에 실패하였습니다')

    def member_remove_member(self):
        id = input('>> id : ')
        if self.ms.remove_member(id):
            print('회원탈퇴가 완료되었습니다')
        else: 
            print('회원탈퇴에 실패하였습니다')

    def show_welcome(self): # ========== Member Manager ==========
            print('=' * 50)
            title = 'Member Manager'
            print(f'{title:^50}')
            print('=' * 50)

    def say_goodbye(self):
        print('안녕히 가세요')

    def print_menu(self, menu_list):
        print('-' * 50)
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}')
        print(f'0. {menu_list[0]}')
        print('-' * 50)

    def select_menu(self, menu_list):
        self.print_menu(menu_list)
        try:
            menu = int(input('메뉴 선택 : '))
            return menu
        except ValueError:
            return -1

if __name__ == '__main__':
    app = MemberManager()
    app.main()
