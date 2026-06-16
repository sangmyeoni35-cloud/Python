# service.py - Service 계층 (비즈니스 로직 담당)

from models import Member, Book, Cart, Order
from dao import MemberDAO, BookDAO, OrderDAO


class MemberService:
    def __init__(self):
        self.dao = MemberDAO()
        self.current = None  # 현재 로그인 회원

    def login(self, email, password):
        member = self.dao.find_by_email(email)
        if member is None:
            return False, "이메일이 존재하지 않습니다."
        if member.password != password:
            return False, "비밀번호가 틀렸습니다."
        self.current = member
        return True, f"{member.name}님 환영합니다!"

    def logout(self):
        self.current = None

    def create_member(self, name, email, password):
        if self.dao.find_by_email(email):
            return False, "이미 사용 중인 이메일입니다."
        if len(password) < 4:
            return False, "비밀번호는 4자 이상이어야 합니다."
        member = Member(self.dao.next_id(), name, email, password)
        self.dao.insert(member)
        return True, "회원가입 완료!"

    def update_profile(self, name, password):
        self.current.name = name
        self.current.password = password
        self.dao.insert(self.current)
        return True, "정보가 수정되었습니다."

    def get_all(self):
        return self.dao.find_all()

    def delete(self, user_id):
        if self.dao.delete(user_id):
            return True, f"{user_id} 삭제 완료"
        return False, "존재하지 않는 회원입니다."


class BookService:
    def __init__(self):
        self.dao = BookDAO()
        self.order_dao = OrderDAO()
        self.cart = Cart()

    def get_all(self):
        return self.dao.find_all()

    def search(self, keyword):
        if not keyword:
            return self.dao.find_all()
        return self.dao.find_by_keyword(keyword)

    def create_book(self, title, author, price, stock):
        try:
            price = int(price)
            stock = int(stock)
        except ValueError:
            return False, "가격과 재고는 숫자로 입력해주세요."
        book = Book(self.dao.next_id(), title, author, price, stock)
        self.dao.insert(book)
        return True, f"도서 등록 완료! (ID: {book.book_id})"

    def delete_book(self, book_id):
        if self.dao.delete(book_id):
            return True, f"{book_id} 삭제 완료"
        return False, "존재하지 않는 도서입니다."

    def add_to_cart(self, book_id):
        book = self.dao.find_by_id(book_id)
        if book is None:
            return False, "존재하지 않는 도서입니다."
        if book.stock <= 0:
            return False, "재고가 없습니다."
        self.cart.add_item(book)
        return True, f"'{book.title}' 담겼습니다."

    def remove_from_cart(self, book_id):
        self.cart.remove_item(book_id)
        return True, "삭제되었습니다."

    def create_order(self, member_id):
        if not self.cart.items:
            return False, "장바구니가 비어 있습니다."
        order = Order(self.order_dao.next_id(), member_id)
        self.order_dao.insert(order)
        for item in self.cart.items:
            item['book'].stock -= item['qty']
        self.cart.clear()
        return True, f"주문 완료! 주문번호: {order.order_id}"

    def get_orders(self, member_id):
        return self.order_dao.find_by_member(member_id)
