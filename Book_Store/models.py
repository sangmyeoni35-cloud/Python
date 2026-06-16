# models.py - 도메인 모델

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return f"[{self.user_id}] {self.name}"


class NonMember(User):
    def __init__(self, session_id):
        self.user_id = ""
        self.name = "비회원"
        self.session_id = session_id


class Member(User):
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def __str__(self):
        return f"[{self.user_id}] {self.name} ({self.email})"


class Admin(User):
    def __init__(self, admin_id, name):
        self.user_id = admin_id
        self.name = name
        self.admin_id = admin_id

    def __str__(self):
        return f"[관리자] {self.name}"


class Book:
    def __init__(self, book_id, title, author, price, stock):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

    def get_info(self):
        return f"[{self.book_id}] {self.title} / {self.author} / {self.price:,}원 / 재고:{self.stock}"

    def check_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.get_info()


class Cart:
    def __init__(self):
        self.items = []  # {'book': Book, 'qty': int}

    def add_item(self, book, qty=1):
        for item in self.items:
            if item['book'].book_id == book.book_id:
                item['qty'] += qty
                return
        self.items.append({'book': book, 'qty': qty})

    def remove_item(self, book_id):
        self.items = [i for i in self.items if i['book'].book_id != book_id]

    def total_price(self):
        return sum(i['book'].price * i['qty'] for i in self.items)

    def clear(self):
        self.items = []


class Order:
    def __init__(self, order_id, member_id, status="주문완료"):
        self.order_id = order_id
        self.member_id = member_id
        self.status = status

    def __str__(self):
        return f"[{self.order_id}] 회원:{self.member_id} / 상태:{self.status}"
