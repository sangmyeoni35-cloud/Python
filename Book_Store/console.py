# console.py - Console 계층 (화면 입출력 담당)

from service import MemberService, BookService


class Console:
    def __init__(self):
        self.member_svc = MemberService()
        self.book_svc = BookService()

    # ── 공통 출력 ──────────────────────────────────────

    def header(self, title):
        print("\n" + "=" * 40)
        print(f"  {title}")
        print("=" * 40)

    def pause(self):
        input("  [Enter] 계속...")

    # ── 실행 ──────────────────────────────────────────

    def run(self):
        while True:
            self.header("📚 온라인 서점")
            print("  1. 로그인")
            print("  2. 회원가입")
            print("  3. 도서 검색")
            print("  4. 관리자 로그인")
            print("  0. 종료")
            choice = input("  선택: ")

            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                self.search_books()
            elif choice == "4":
                self.admin_login()
            elif choice == "0":
                print("  종료합니다.")
                break

    # ── 인증 ──────────────────────────────────────────

    def login(self):
        self.header("로그인")
        email = input("  이메일: ")
        password = input("  비밀번호: ")
        ok, msg = self.member_svc.login(email, password)
        print(f"  {msg}")
        if ok:
            self.pause()
            self.member_menu()

    def register(self):
        self.header("회원가입")
        name = input("  이름: ")
        email = input("  이메일: ")
        password = input("  비밀번호: ")
        ok, msg = self.member_svc.create_member(name, email, password)
        print(f"  {msg}")
        self.pause()

    def admin_login(self):
        self.header("관리자 로그인")
        email = input("  이메일: ")
        password = input("  비밀번호: ")
        if email == "admin@store.com" and password == "admin00":
            print("  관리자 로그인 성공")
            self.pause()
            self.admin_menu()
        else:
            print("  관리자 정보가 틀렸습니다.")
            self.pause()

    # ── 회원 메뉴 ─────────────────────────────────────

    def member_menu(self):
        while True:
            name = self.member_svc.current.name
            self.header(f"회원 메뉴 ({name})")
            print("  1. 도서 검색")
            print("  2. 장바구니 담기")
            print("  3. 장바구니 보기")
            print("  4. 주문하기")
            print("  5. 주문 내역")
            print("  6. 정보 수정")
            print("  0. 로그아웃")
            choice = input("  선택: ")

            if choice == "1":
                self.search_books()
            elif choice == "2":
                self.add_to_cart()
            elif choice == "3":
                self.view_cart()
            elif choice == "4":
                self.place_order()
            elif choice == "5":
                self.view_orders()
            elif choice == "6":
                self.update_profile()
            elif choice == "0":
                self.member_svc.logout()
                print("  로그아웃 되었습니다.")
                break

    # ── 도서 기능 ─────────────────────────────────────

    def search_books(self):
        self.header("도서 검색")
        keyword = input("  검색어 (전체: Enter): ")
        books = self.book_svc.search(keyword)
        if not books:
            print("  검색 결과 없음")
        else:
            for b in books:
                print(f"  {b}")
        self.pause()

    def add_to_cart(self):
        self.header("장바구니 담기")
        for b in self.book_svc.get_all():
            print(f"  {b}")
        book_id = input("  도서 ID: ")
        ok, msg = self.book_svc.add_to_cart(book_id)
        print(f"  {msg}")
        self.pause()

    def view_cart(self):
        self.header("장바구니")
        cart = self.book_svc.cart
        if not cart.items:
            print("  비어 있습니다.")
        else:
            for item in cart.items:
                b = item['book']
                print(f"  [{b.book_id}] {b.title} x{item['qty']} = {b.price * item['qty']:,}원")
            print(f"  합계: {cart.total_price():,}원")
            print("  d. 도서 삭제 | 그 외: 돌아가기")
            if input("  선택: ").lower() == "d":
                book_id = input("  삭제할 도서 ID: ")
                ok, msg = self.book_svc.remove_from_cart(book_id)
                print(f"  {msg}")
        self.pause()

    def place_order(self):
        self.header("주문하기")
        cart = self.book_svc.cart
        if not cart.items:
            print("  장바구니가 비어 있습니다.")
        else:
            print(f"  합계: {cart.total_price():,}원")
            if input("  주문하시겠습니까? (y/n): ").lower() == "y":
                ok, msg = self.book_svc.create_order(self.member_svc.current.user_id)
                print(f"  {msg}")
            else:
                print("  취소되었습니다.")
        self.pause()

    def view_orders(self):
        self.header("주문 내역")
        orders = self.book_svc.get_orders(self.member_svc.current.user_id)
        if not orders:
            print("  주문 내역이 없습니다.")
        else:
            for o in orders:
                print(f"  {o}")
        self.pause()

    def update_profile(self):
        self.header("정보 수정")
        name = input(f"  이름 ({self.member_svc.current.name}): ")
        password = input("  새 비밀번호: ")
        if not name:
            name = self.member_svc.current.name
        if not password:
            password = self.member_svc.current.password
        ok, msg = self.member_svc.update_profile(name, password)
        print(f"  {msg}")
        self.pause()

    # ── 관리자 메뉴 ───────────────────────────────────

    def admin_menu(self):
        while True:
            self.header("관리자 메뉴")
            print("  1. 회원 목록")
            print("  2. 회원 삭제")
            print("  3. 도서 등록")
            print("  4. 도서 삭제")
            print("  5. 전체 도서 목록")
            print("  0. 로그아웃")
            choice = input("  선택: ")

            if choice == "1":
                self.header("회원 목록")
                for m in self.member_svc.get_all():
                    print(f"  {m}")
                self.pause()
            elif choice == "2":
                self.header("회원 삭제")
                for m in self.member_svc.get_all():
                    print(f"  {m}")
                uid = input("  삭제할 회원 ID: ")
                ok, msg = self.member_svc.delete(uid)
                print(f"  {msg}")
                self.pause()
            elif choice == "3":
                self.header("도서 등록")
                title = input("  제목: ")
                author = input("  저자: ")
                price = input("  가격: ")
                stock = input("  재고: ")
                ok, msg = self.book_svc.create_book(title, author, price, stock)
                print(f"  {msg}")
                self.pause()
            elif choice == "4":
                self.header("도서 삭제")
                for b in self.book_svc.get_all():
                    print(f"  {b}")
                bid = input("  삭제할 도서 ID: ")
                ok, msg = self.book_svc.delete_book(bid)
                print(f"  {msg}")
                self.pause()
            elif choice == "5":
                self.header("전체 도서 목록")
                for b in self.book_svc.get_all():
                    print(f"  {b}")
                self.pause()
            elif choice == "0":
                print("  관리자 로그아웃")
                break
