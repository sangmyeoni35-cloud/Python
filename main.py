class Console:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    RESET = "\033[0m"

    def __init__(self, member_service, company_service, repair_service, payment_service, review_service, admin_service):
        self.member_service = member_service
        self.company_service = company_service
        self.repair_service = repair_service
        self.payment_service = payment_service
        self.review_service = review_service
        self.admin_service = admin_service
        self.login_member = None
        self.login_company = None
        self.login_admin = None

    def line(self):
        print("=" * 44)

    def title(self, text):
        self.line()
        print(f"{text:^38}")
        self.line()

    def guide(self, text):
        print(f"{self.GREEN}{text}{self.RESET}")

    def warn(self, text):
        print(f"{self.RED}{text}{self.RESET}")

    def pause(self):
        input("\n계속하려면 Enter...")

    def run(self):
        self.seed_data()
        while True:
            self.title("안전결제 기반 집수리 중개 플랫폼")
            print("1. 고객 메뉴")
            print("2. 업체 메뉴")
            print("3. 관리자 메뉴")
            print("0. 종료")
            choice = input("\n선택 > ")

            if choice == "1":
                self.member_menu()
            elif choice == "2":
                self.company_menu()
            elif choice == "3":
                self.admin_menu()
            elif choice == "0":
                self.guide("프로그램을 종료합니다.")
                break
            else:
                self.warn("잘못된 입력입니다.")

    def seed_data(self):
        """
        발표 시연용 기본 데이터 자동 생성
        관리자 메뉴를 먼저 실행해도 회원목록, 결제목록, 입금확인, 정산완료 자료가 나오도록 구성합니다.
        """
        if len(self.company_service.list_companies()) == 0:
            c1 = self.company_service.join(
                "gangnam", "1234", "강남전기", "김기사",
                "111-22-33333", "조명", "010-1111-1111", "서울시 강남구 테헤란로 10"
            )
            c2 = self.company_service.join(
                "shine", "1234", "빛나는조명", "박기사",
                "222-33-44444", "조명", "010-2222-2222", "서울시 서초구 반포대로 20"
            )
            c3 = self.company_service.join(
                "newlight", "1234", "행복조명", "이조명",
                "333-44-55555", "조명", "010-5555-1111", "서울시 송파구"
            )

            self.company_service.approve_company(c1.company_id)
            self.company_service.approve_company(c2.company_id)
            # c3는 관리자 업체승인 시연용으로 승인대기 상태 유지

        if len(self.member_service.list_members()) == 0:
            demo_member = self.member_service.join(
                "hong", "1234", "홍길동", "010-1234-5678", "서울시 강남구 역삼동 100-1"
            )

            demo_request = self.repair_service.create_request(
                demo_member.member_id,
                "조명",
                "거실등 교체 요청",
                "거실 LED 등이 고장났습니다.",
                "서울시 강남구 역삼동 100-1"
            )

            demo_contract = self.repair_service.select_company(
                demo_request.request_id,
                demo_member.member_id,
                1,
                100000
            )

            demo_payment = self.payment_service.pay(
                demo_contract.contract_id,
                demo_member.member_id,
                1,
                100000
            )

            # 관리자 정산완료 처리 시연용 정산 데이터 1건 생성
            # 결제번호 1, 정산번호 1을 바로 사용할 수 있습니다.
            from model import Settlement
            demo_settlement = Settlement(
                self.payment_service.settlement_dao.next_id(),
                demo_payment.payment_id,
                1,
                demo_payment.payment_amount,
                demo_payment.fee_amount,
                demo_payment.settlement_amount,
                status="정산대기"
            )
            self.payment_service.settlement_dao.settlements.append(demo_settlement)

    # ===================== 고객 메뉴 =====================
    def member_menu(self):
        while True:
            self.title("고객(회원) 메뉴")
            print("1. 회원가입")
            print("2. 로그인")
            print("3. 수리요청 등록")
            print("4. 업체 검색/목록")
            print("5. 업체 선택 및 계약")
            print("6. 안전결제")
            print("7. 완료승인 및 정산요청")
            print("8. 리뷰 작성")
            print("9. 나의 요청 목록")
            print("0. 뒤로가기")
            choice = input("\n선택 > ")

            try:
                if choice == "1":
                    self.member_join()
                elif choice == "2":
                    self.member_login()
                elif choice == "3":
                    self.create_request()
                elif choice == "4":
                    self.search_company()
                elif choice == "5":
                    self.create_contract()
                elif choice == "6":
                    self.create_payment()
                elif choice == "7":
                    self.approve_complete()
                elif choice == "8":
                    self.write_review()
                elif choice == "9":
                    self.my_requests()
                elif choice == "0":
                    break
                else:
                    self.warn("잘못된 입력입니다.")
            except Exception as e:
                self.warn(f"오류: {e}")
                self.pause()

    def member_join(self):
        self.title("회원가입")
        login_id = input("아이디 : ")
        password = input("비밀번호 : ")
        name = input("이름 : ")
        phone = input("전화번호 : ")
        address = input("주소 : ")
        member = self.member_service.join(login_id, password, name, phone, address)

        print()
        print(f"이름 : {member.name}")
        print(f"아이디 : {member.login_id}")
        print(f"전화번호 : {member.phone}")
        print(f"주소 : {member.address}")
        self.guide("\n회원가입이 완료되었습니다.")
        self.pause()

    def member_login(self):
        self.title("로그인")
        login_id = input("아이디 : ")
        password = input("비밀번호 : ")
        member = self.member_service.login(login_id, password)

        if member:
            self.login_member = member
            self.guide("\n로그인 성공!")
            self.guide(f"{member.name}님 환영합니다.")
        else:
            self.warn("\n로그인 실패! 아이디 또는 비밀번호를 확인하세요.")
        self.pause()

    def create_request(self):
        self.check_member()
        self.title("수리요청 작성")
        category = input("카테고리 : ")
        title = input("제목 : ")
        content = input("내용 : ")
        address = input("주소 : ")

        request = self.repair_service.create_request(
            self.login_member.member_id, category, title, content, address
        )

        print()
        print(f"카테고리 : {request.category}")
        print(f"제목 : {request.title}")
        print(f"내용 : {request.content}")
        print(f"주소 : {request.address}")
        print(f"요청번호 : {request.request_id}")
        self.guide("\n수리요청이 등록되었습니다.")
        self.pause()

    def search_company(self):
        self.title("업체 검색 결과")
        category = input("검색할 수리항목 : ")
        companies = self.company_service.search_by_category(category)

        if not companies:
            self.warn("\n조회된 업체가 없습니다.")
            self.pause()
            return

        print()
        for idx, company in enumerate(companies, start=1):
            print(f"{idx}. 업체번호 : {company.company_id}")
            print(f"   업체명 : {company.company_name}")
            print(f"   대표자 : {company.ceo_name}")
            print(f"   연락처 : {company.phone}")
            print(f"   주소 : {company.address}")
            print(f"   평점 : {company.rating}")
            print(f"   승인상태 : {company.approval_status}")
            print("-" * 44)

        self.guide("원하는 업체번호를 기억한 뒤 계약 메뉴에서 선택하세요.")
        self.pause()

    def create_contract(self):
        self.check_member()
        self.title("계약 확인")
        request_id = int(input("요청번호 : "))
        company_id = int(input("선택할 업체번호 : "))
        amount = int(input("수리금액 : "))

        contract = self.repair_service.select_company(
            request_id, self.login_member.member_id, company_id, amount
        )

        print()
        print(f"계약번호 : {contract.contract_id}")
        print(f"요청번호 : {contract.request_id}")
        print(f"업체번호 : {contract.company_id}")
        print(f"계약금액 : {contract.agreed_amount:,}원")
        print(f"계약상태 : {contract.status}")
        self.guide("\n계약이 생성되었습니다.")
        self.pause()

    def create_payment(self):
        self.check_member()
        self.title("안전결제")
        contract_id = int(input("계약번호 : "))
        amount = int(input("결제금액 : "))

        payment = self.payment_service.pay(contract_id, self.login_member.member_id, 1, amount)

        print()
        print(f"결제번호 : {payment.payment_id}")
        print(f"계약번호 : {payment.contract_id}")
        print(f"결제금액 : {payment.payment_amount:,}원")
        print(f"수수료(3%) : {payment.fee_amount:,}원")
        print(f"업체정산금(97%) : {payment.settlement_amount:,}원")
        print(f"결제상태 : {payment.status}")
        self.guide("\n안전결제가 등록되었습니다.")
        self.guide("관리자가 입금확인을 해야 다음 단계로 진행됩니다.")
        self.pause()

    def approve_complete(self):
        self.title("수리 완료 승인")
        payment_id = int(input("결제번호 : "))
        company_id = int(input("업체번호 : "))

        settlement = self.payment_service.approve_complete_and_settle(payment_id, company_id)

        print()
        print(f"정산번호 : {settlement.settlement_id}")
        print(f"결제번호 : {settlement.payment_id}")
        print(f"업체번호 : {settlement.company_id}")
        print(f"정산금액 : {settlement.settlement_amount:,}원")
        print(f"정산상태 : {settlement.status}")
        self.guide("\n수리 완료 승인이 처리되었습니다.")
        self.guide("정산요청이 생성되었습니다.")
        self.pause()

    def write_review(self):
        self.check_member()
        self.title("리뷰 작성")
        contract_id = int(input("계약번호 : "))
        company_id = int(input("업체번호 : "))
        rating = int(input("별점(1~5) : "))
        content = input("리뷰내용 : ")

        review = self.review_service.write_review(
            contract_id, self.login_member.member_id, company_id, rating, content
        )

        print()
        print(f"리뷰번호 : {review.review_id}")
        print(f"별점 : {review.rating}")
        print(f"내용 : {review.content}")
        self.guide("\n리뷰가 등록되었습니다.")
        self.pause()

    def my_requests(self):
        self.check_member()
        self.title("나의 요청 목록")
        requests = self.repair_service.request_dao.find_by_member(self.login_member.member_id)
        if not requests:
            self.warn("등록된 요청이 없습니다.")
        for r in requests:
            print(f"{r.request_id}. [{r.status}] {r.title} / {r.category} / {r.address}")
        self.pause()

    # ===================== 업체 메뉴 =====================
    def company_menu(self):
        while True:
            self.title("업체 메뉴")
            print("1. 업체가입")
            print("2. 로그인")
            print("3. 수리요청 목록")
            print("4. 진행중 계약 목록")
            print("5. 작업완료 처리")
            print("6. 정산 내역 조회")
            print("0. 뒤로가기")
            choice = input("\n선택 > ")

            try:
                if choice == "1":
                    self.company_join()
                elif choice == "2":
                    self.company_login()
                elif choice == "3":
                    self.list_requests()
                elif choice == "4":
                    self.list_company_contracts()
                elif choice == "5":
                    self.company_complete_work()
                elif choice == "6":
                    self.list_settlements_by_company()
                elif choice == "0":
                    break
                else:
                    self.warn("잘못된 입력입니다.")
            except Exception as e:
                self.warn(f"오류: {e}")
                self.pause()

    def company_join(self):
        self.title("업체가입")
        login_id = input("아이디 : ")
        password = input("비밀번호 : ")
        company_name = input("업체명 : ")
        ceo_name = input("대표자 : ")
        business_no = input("사업자번호 : ")
        category = input("전문분야 : ")
        phone = input("전화번호 : ")
        address = input("주소 : ")

        company = self.company_service.join(
            login_id, password, company_name, ceo_name,
            business_no, category, phone, address
        )

        print()
        print(f"업체번호 : {company.company_id}")
        print(f"업체명 : {company.company_name}")
        print(f"전문분야 : {company.category}")
        print(f"승인상태 : {company.approval_status}")
        self.guide("\n업체가입이 완료되었습니다.")
        self.guide("관리자 승인이 필요합니다.")
        self.pause()

    def company_login(self):
        self.title("업체 로그인")
        login_id = input("아이디 : ")
        password = input("비밀번호 : ")
        company = self.company_service.login(login_id, password)

        if company:
            self.login_company = company
            self.guide("\n로그인 성공!")
            self.guide(f"{company.company_name}님 환영합니다.")
        else:
            self.warn("\n로그인 실패")
        self.pause()

    def list_requests(self):
        self.title("수리요청 목록")
        requests = self.repair_service.list_requests()
        if not requests:
            self.warn("등록된 수리요청이 없습니다.")
        for r in requests:
            print(f"{r.request_id}. [{r.status}] {r.title}")
            print(f"   고객번호 : {r.member_id}")
            print(f"   수리항목 : {r.category}")
            print(f"   주소 : {r.address}")
            print(f"   내용 : {r.content}")
            print("-" * 44)
        self.pause()

    def list_company_contracts(self):
        self.check_company()
        self.title("진행중 계약 목록")
        contracts = self.repair_service.contract_dao.find_by_company(self.login_company.company_id)
        if not contracts:
            self.warn("진행중 계약이 없습니다.")
        for c in contracts:
            print(f"계약번호 : {c.contract_id}")
            print(f"요청번호 : {c.request_id}")
            print(f"계약금액 : {c.agreed_amount:,}원")
            print(f"상태 : {c.status}")
            print("-" * 44)
        self.pause()

    def company_complete_work(self):
        self.check_company()
        self.title("작업완료 처리")
        contract_id = int(input("계약번호 : "))
        contract = self.repair_service.complete_work(contract_id)

        print()
        print(f"계약번호 : {contract.contract_id}")
        print(f"상태 : {contract.status}")
        self.guide("\n작업완료 처리되었습니다.")
        self.pause()

    def list_settlements_by_company(self):
        self.check_company()
        self.title("정산 내역 조회")
        settlements = self.payment_service.settlement_dao.find_by_company(self.login_company.company_id)

        if not settlements:
            self.warn("정산 내역이 없습니다.")
        for s in settlements:
            print(f"정산번호 : {s.settlement_id}")
            print(f"결제금액 : {s.payment_amount:,}원")
            print(f"수수료 : {s.fee_amount:,}원")
            print(f"정산금액 : {s.settlement_amount:,}원")
            print(f"정산상태 : {s.status}")
            print("-" * 44)
        self.pause()

    # ===================== 관리자 메뉴 =====================
    def admin_menu(self):
        while True:
            self.title("관리자 메뉴")
            print("1. 로그인")
            print("2. 회원 목록 조회")
            print("3. 업체 목록 조회")
            print("4. 업체 승인")
            print("5. 결제 목록 조회")
            print("6. 입금 확인  ※ 시연용 결제번호 1")
            print("7. 정산 완료 처리  ※ 시연용 정산번호 1")
            print("8. 통계 조회")
            print("0. 뒤로가기")
            choice = input("\n선택 > ")

            try:
                if choice == "1":
                    self.admin_login()
                elif choice == "2":
                    self.list_members_admin()
                elif choice == "3":
                    self.list_companies_admin()
                elif choice == "4":
                    self.approve_company_admin()
                elif choice == "5":
                    self.list_payments_admin()
                elif choice == "6":
                    self.confirm_payment_admin()
                elif choice == "7":
                    self.complete_settlement_admin()
                elif choice == "8":
                    self.statistics_admin()
                elif choice == "0":
                    break
                else:
                    self.warn("잘못된 입력입니다.")
            except Exception as e:
                self.warn(f"오류: {e}")
                self.pause()

    def admin_login(self):
        self.title("관리자 로그인")
        login_id = input("아이디 : ")
        password = input("비밀번호 : ")

        admin = self.admin_service.login(login_id, password)
        if admin:
            self.login_admin = admin
            self.guide("\n로그인 성공!")
            self.guide(f"{admin.name}님 환영합니다.")
        else:
            self.warn("\n관리자 로그인 실패")
        self.pause()

    def list_members_admin(self):
        self.title("회원 목록")
        members = self.member_service.list_members()
        if not members:
            self.warn("등록된 회원이 없습니다.")
        for m in members:
            print(f"회원번호 : {m.member_id}")
            print(f"아이디 : {m.login_id}")
            print(f"이름 : {m.name}")
            print(f"전화번호 : {m.phone}")
            print(f"주소 : {m.address}")
            print("-" * 44)
        self.pause()

    def list_companies_admin(self):
        self.title("업체 목록")
        companies = self.company_service.list_companies()
        if not companies:
            self.warn("등록된 업체가 없습니다.")
        for c in companies:
            print(f"업체번호 : {c.company_id}")
            print(f"업체명 : {c.company_name}")
            print(f"전문분야 : {c.category}")
            print(f"승인상태 : {c.approval_status}")
            print("-" * 44)
        self.pause()

    def approve_company_admin(self):
        self.title("업체 승인")
        company_id = int(input("승인할 업체번호 : "))
        company = self.company_service.approve_company(company_id)

        if company:
            print(f"업체명 : {company.company_name}")
            print(f"승인상태 : {company.approval_status}")
            self.guide("\n업체승인이 완료되었습니다.")
        else:
            self.warn("업체를 찾을 수 없습니다.")
        self.pause()

    def list_payments_admin(self):
        self.title("결제 목록")
        payments = self.payment_service.list_payments()
        if not payments:
            self.warn("결제 내역이 없습니다.")
        for p in payments:
            print(f"결제번호 : {p.payment_id}")
            print(f"계약번호 : {p.contract_id}")
            print(f"결제금액 : {p.payment_amount:,}원")
            print(f"수수료(3%) : {p.fee_amount:,}원")
            print(f"업체정산금(97%) : {p.settlement_amount:,}원")
            print(f"상태 : {p.status}")
            print("-" * 44)
        self.pause()

    def confirm_payment_admin(self):
        self.title("입금 확인")
        payment_id = int(input("입금 확인할 결제번호 : "))
        payment = self.payment_service.confirm_payment(payment_id)

        if payment:
            print(f"결제번호 : {payment.payment_id}")
            print(f"결제금액 : {payment.payment_amount:,}원")
            print(f"수수료(3%) : {payment.fee_amount:,}원")
            print(f"업체정산금(97%) : {payment.settlement_amount:,}원")
            print(f"결제상태 : {payment.status}")
            self.guide("\n입금 확인 처리되었습니다.")
        else:
            self.warn("결제 정보를 찾을 수 없습니다.")
        self.pause()

    def complete_settlement_admin(self):
        self.title("정산 관리")
        settlement_id = int(input("정산번호 : "))
        settlement = self.payment_service.complete_settlement(settlement_id)

        if settlement:
            print(f"정산번호 : {settlement.settlement_id}")
            print(f"정산금액 : {settlement.settlement_amount:,}원")
            print(f"정산상태 : {settlement.status}")
            self.guide("\n정산완료 처리되었습니다.")
        else:
            self.warn("정산 정보를 찾을 수 없습니다.")
        self.pause()

    def statistics_admin(self):
        self.title("플랫폼 통계")
        stats = self.admin_service.statistics()
        for key, value in stats.items():
            if isinstance(value, int):
                print(f"{key} : {value:,}")
            else:
                print(f"{key} : {value}")
        self.guide("\n모든 통계가 정상적으로 조회되었습니다.")
        self.pause()

    # ===================== 로그인 체크 =====================
    def check_member(self):
        if not self.login_member:
            raise ValueError("고객 로그인이 필요합니다.")

    def check_company(self):
        if not self.login_company:
            raise ValueError("업체 로그인이 필요합니다.")
