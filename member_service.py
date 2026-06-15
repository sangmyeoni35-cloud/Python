from member import Member
# from member_dao import MemberDAO

#====================================
# 회원 관리 서비스 로직 (Controller) : MemberService
class MemberService:
    ADMIN_ID = 'admin'      # 관리자 계정 아이디
    ADMIN_PASSWORD = '1234' # 관리자 계정 비밀번호
    member_no_seq = 100     # 자동 회원번호

    def __init__(self, memberDao):
        self.__dao = memberDao 
        self.current_user = None # 현재 로그인 중인 계정(관리자인지 아닌지)
        # 시작과 동시에 관리자 계정 미리 생성
        self.join(Member(None, MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD, '관리자'))

    def login(self, id, password): # 로그인
            member = self.__dao.get_member_info(id) # 아이디에 해당하는 회원정보를 저장
            if member:
                if password == member.get_password(): # 그 회원정보에 저장된 비번과 입력받은 비번이 같으면
                    self.current_user = id # 현재 로그인 중인 계정을 이 회원 아이디로 바꿈
                    return True
            return False

    def join(self, member): # 회원가입
        
        # 대소문자 구별하지 않음
        # member.set_id(member.get_id().lower())
        # if not self.is_valid_id(member.get_id()):
        #     return False

        # 이미 있는 아이디인지 확인
        if self.__dao.is_exist(member.get_id()):
            return False
        member.set_member_no(MemberService.member_no_seq)
        MemberService.member_no_seq += 1
        self.__dao.insert_member(member)
        return True
    
    # def is_valid_id(self, id):
    #     # 아이디가 유효한지 확인
    #     if id.isalpha(): return True
    
    def logout(self): # 로그아웃
        self.current_user = None # 그냥 현재 접속 계정 None으로 바꿈

    def list_members(self): # 회원 목록
        return self.__dao.get_all_members()

    def view_member_info(self, id): # 내(회원) 정보 조회
        return self.__dao.get_member_info(id) 
    
    def remove_member(self, id): # 회원 탈퇴(강퇴)
        if self.current_user == id or self.current_user == MemberService.ADMIN_ID: # 본인이거나 관리자라면
            return self.__dao.remove_member(id) # 해당 아이디 계정 삭제
        return False
    
    def update_member_info(self, id, member): # 정보 수정(밑에 아이디, 패스워드)
        return self.__dao.update_member_info(id, member) 
    
    def update_member_id(self, org_id, new_id): # 아이디 수정
        id = org_id
        if self.current_user != id: return False
        member = self.__dao.get_member_info(id)
        if not member: return False
        if member.get_id() == org_id:
            member.set_id(new_id)
            self.current_user = new_id
            return True
        return False
    
    def update_member_password(self, id, org_password, new_password): # 비밀번호 수정
        if self.current_user != id: return False
        member = self.__dao.get_member_info(id)
        if not member: return False
        if member.get_password() == org_password: # 원래 비번이 일치하면
            member.set_password(new_password) # 새 비번으로 바꿔서 저장
            return True
        return False

    
# if __name__ == '__main__':
#     ms = MemberService(MemberDAO())
#     ms.join(Member('hyejeong', '1234', '이혜정'))
#     ms.join(Member('curi', '1111', '큐리'))
#     members = ms.list_members()
#     for member in members:
#         print(member)
#     ms.login('curi', '1111')
#     print(ms.current_user)
#     ms.logout()
#     print(ms.current_user)
#     print(ms.view_member_info('curi'))
#     ms.login(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD)
#     print(ms.update_member_password('hyejeong', '1234', '4321'))
#     print(ms.view_member_info('hyejeong'))
#     print(ms.remove_member('hyejeong'))
#     print(ms.view_member_info('hyejeong'))