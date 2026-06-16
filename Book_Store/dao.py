# dao.py - DAO 계층 (데이터 저장/조회 담당)

from models import Member, Book, Order


class MemberDAO:
    def __init__(self):
        self.db = {}
        # 샘플 데이터
        m = Member("M001", "홍길동", "hong@email.com", "1234")
        self.db[m.user_id] = m

    def insert(self, member):
        self.db[member.user_id] = member

    def find_by_id(self, user_id):
        return self.db.get(user_id)

    def find_by_email(self, email):
        for m in self.db.values():
            if m.email == email:
                return m
        return None

    def find_all(self):
        return list(self.db.values())

    def delete(self, user_id):
        if user_id in self.db:
            del self.db[user_id]
            return True
        return False

    def next_id(self):
        return "M" + str(len(self.db) + 1).zfill(3)


class BookDAO:
    def __init__(self):
        self.db = {}
        # 샘플 데이터
        samples = [
            Book("B001", "파이썬 완전 정복", "김철수", 28000, 10),
            Book("B002", "자료구조와 알고리즘", "이영희", 32000, 5),
            Book("B003", "클린 코드", "로버트 마틴", 26000, 8),
            Book("B004", "데이터베이스 개론", "박민준", 30000, 0),
        ]
        for b in samples:
            self.db[b.book_id] = b

    def insert(self, book):
        self.db[book.book_id] = book

    def find_by_id(self, book_id):
        return self.db.get(book_id)

    def find_all(self):
        return list(self.db.values())

    def find_by_keyword(self, keyword):
        kw = keyword.lower()
        return [b for b in self.db.values()
                if kw in b.title.lower() or kw in b.author.lower()]

    def delete(self, book_id):
        if book_id in self.db:
            del self.db[book_id]
            return True
        return False

    def next_id(self):
        return "B" + str(len(self.db) + 1).zfill(3)


class OrderDAO:
    def __init__(self):
        self.db = {}
        self.count = 0

    def insert(self, order):
        self.db[order.order_id] = order

    def find_by_member(self, member_id):
        return [o for o in self.db.values() if o.member_id == member_id]

    def next_id(self):
        self.count += 1
        return "ORD" + str(self.count).zfill(3)
