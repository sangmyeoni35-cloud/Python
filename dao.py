from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Member:
    member_id: int
    login_id: str
    password: str
    name: str
    phone: str
    address: str
    created_at: str = datetime.now().strftime("%Y-%m-%d")


@dataclass
class Company:
    company_id: int
    login_id: str
    password: str
    company_name: str
    ceo_name: str
    business_no: str
    category: str
    phone: str
    address: str
    rating: float = 0.0
    approval_status: str = "대기"
    created_at: str = datetime.now().strftime("%Y-%m-%d")


@dataclass
class Admin:
    admin_id: int
    login_id: str
    password: str
    name: str
    phone: str
    role: str = "관리자"


@dataclass
class RepairRequest:
    request_id: int
    member_id: int
    category: str
    title: str
    content: str
    address: str
    request_date: str = datetime.now().strftime("%Y-%m-%d")
    status: str = "요청등록"


@dataclass
class Contract:
    contract_id: int
    request_id: int
    member_id: int
    company_id: int
    agreed_amount: int
    contract_date: str = datetime.now().strftime("%Y-%m-%d")
    status: str = "계약생성"


@dataclass
class Payment:
    payment_id: int
    contract_id: int
    member_id: int
    admin_id: int
    payment_amount: int
    fee_amount: int
    settlement_amount: int
    payment_date: str = datetime.now().strftime("%Y-%m-%d")
    status: str = "입금대기"


@dataclass
class Settlement:
    settlement_id: int
    payment_id: int
    company_id: int
    payment_amount: int
    fee_amount: int
    settlement_amount: int
    settlement_date: str = datetime.now().strftime("%Y-%m-%d")
    status: str = "정산대기"


@dataclass
class Review:
    review_id: int
    contract_id: int
    member_id: int
    company_id: int
    rating: int
    content: str
    created_at: str = datetime.now().strftime("%Y-%m-%d")


@dataclass
class Notice:
    notice_id: int
    admin_id: int
    title: str
    content: str
    created_at: str = datetime.now().strftime("%Y-%m-%d")
