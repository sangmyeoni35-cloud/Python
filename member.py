# from member_dao import MemberDAO

#==============================
# 데이터 모델 정의 : Member
class Member:
    def __init__(self, member_no, id, password, name):
        self.__member_no = member_no # 회원번호
        self.__id = id               # 아이디
        self.__password = password   # 비밀번호
        self.__name = name           # 이름

    def get_member_no(self):
        return self.__member_no
    def get_id(self):
        return self.__id
    def get_password(self):
        return self.__password
    def get_name(self):
        return self.__name
    
    def set_member_no(self, member_no):
        self.__member_no = member_no
    def set_id(self, id):
        self.__id = id
    def set_password(self, password):
        self.__password = password

    def __str__(self):
        return f'{self.__member_no}\t{self.__id}\t{self.__name}\t{self.__password}'
    
# # 클래스 동작 테스트 (단위테스트, unit test)
# if __name__ == '__main__':
#     dao = MemberDAO()
#     print(dao.is_exist('hyejeong'))

#     member = Member('hyejeong', '1234', '이혜정')
#     dao.insert_member(member)
#     member = Member('curi', '1234', '1234')
#     dao.insert_member(member)
#     print(dao.get_all_members('hyejeong'))
#     print(dao.get_all_members('curi'))

#     members = dao.get_all_members()
#     for member in members:
#         print(member)

#     member = dao.get_member_info('hyejeong')
#     if member:
#         member.set_password('1111')
#         dao.update_member_info('hyejeong', member)

#     members = dao.get_all_members()
#     for member in members:
#         print(member)
    
#     dao.remove_member('hyejeong')