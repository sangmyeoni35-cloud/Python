# import joblib
#================================
# 회원 데이터 접근 (CRUD) : MemberDAO
class MemberDAO:
    def __init__(self):
        # MEMBER_DB_FILE = './db/memberDB.pkl'
        # self.__memberDB = self.__load_memberDB()
        self.__memberDB = {} # 키 : 회원번호, 값 : 객체(member, 회원정보)

    # def __load_memberDB(self):
    #     # 파일이 존재하는지 확인하는 예외처리 추가
    #     try:
    #         self.__memberDB = joblib.load(MemberDAO.MEMBER_DB_FILE)
    #     except FileNotFoundError:
    #         self.__memberDB = {}
        
    # def save_memberDB(self):
    #     if self.__memberDB:
    #         joblib.dump(self.__memberDB, MemberDAO.MEMBER_DB_FILE)

    def is_exist(self, id): # 해당 회원번호가 이미 있는지 확인
        return self.get_member_by_id(id) is not None
    
    def get_member_by_id(self, id): # 아이디로 회원번호 찾기
        for member in self.__memberDB.values():
            if member.get_id() == id:
                return member
        return None

    def insert_member(self, member):    # 회원 추가
        if self.is_exist(member.get_id()):
            return False
        self.__memberDB[member.get_member_no()] = member # 해당 회원번호(키)에 회원정보(객체) 저장
        return True
    
    def get_all_members(self): # 회원 목록
        if self.__memberDB:
            return list(self.__memberDB.values())
        
    def get_member_info(self, id): # 회원(내) 정보 조회
        if self.is_exist(id):
            return self.get_member_by_id(id)
        return None
        
    def remove_member(self, id): # 회원 삭제
        if self.is_exist(id):
            member = self.get_member_by_id(id)
            self.__memberDB.pop(member.get_member_no())
            return True
        return False
    
    def update_member_info(self, id, member): # 회원 정보 수정
        if self.is_exist(id):
            org_member = self.get_member_info(id)
            self.__memberDB[org_member.get_member_no()] = member
            return True
        return False

    