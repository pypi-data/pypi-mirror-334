from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, ClassVar, Union
from .data_types import Date
from decimal import Decimal, ROUND_HALF_UP
import re


class CustomBaseModel(BaseModel):
    rounding_fields: ClassVar[set[str]] = set()
    date_fields: ClassVar[set[str]] = set()

    @staticmethod
    def clean_price(value: str | float | int) -> Decimal:
        if isinstance(value, str):
            clean_value = re.sub(r"[^\d.]", "", value)
            try:
                return Decimal(clean_value)
            except Exception as e:
                raise ValueError(f"Invalid value for price: {value}") from e
        elif isinstance(value, (float, int)):
            return Decimal(str(value))
        return value

    @model_validator(mode="before")
    @classmethod
    def apply_transformations(cls, values):
        from .utils import fix_date_fields, convert_camel_to_snake

        transformed_values = convert_camel_to_snake(values)

        for field in cls.rounding_fields:
            if field in transformed_values and transformed_values[field] is not None:
                cleaned_value = cls.clean_price(transformed_values[field])

                if isinstance(cleaned_value, Decimal) and not cleaned_value.is_finite():
                    cleaned_value = None

                transformed_values[field] = (
                    cleaned_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    if cleaned_value is not None
                    else None
                )

        for field in cls.date_fields:
            if field in transformed_values and transformed_values[field] is not None:
                transformed_values[field] = fix_date_fields(transformed_values[field])

        return transformed_values

    def recursive_process(self, data):
        if isinstance(data, dict):
            new_dict = {}
            for key, value in data.items():
                processed_value = self.recursive_process(value)
                if processed_value not in (None, [], {}):
                    new_dict[key] = processed_value
            return new_dict if new_dict else None

        elif isinstance(data, list):
            new_list = []
            for item in data:
                processed_item = self.recursive_process(item)
                if processed_item not in (None, [], {}):
                    new_list.append(processed_item)
            return new_list if new_list else None

        elif isinstance(data, str):
            stripped = data.strip()
            return stripped if stripped else None

        elif isinstance(data, Decimal):
            return float(data)

        else:
            return data

    def model_dump(self, include: set = None, exclude: set = None):
        data = super().model_dump(include=include, exclude=exclude)
        return self.recursive_process(data)

    model_config = {
        "populate_by_name": True,
        "str_strip_whitespace": True,
        "extra": "allow",
        "arbitrary_types_allowed": True,
    }


class Email(CustomBaseModel):
    email_address: Optional[str] = Field(None, max_length=255)


class Phone(CustomBaseModel):
    phone_number: Optional[str] = Field(None, max_length=255)
    phone_type: Optional[str] = Field(None, max_length=255)
    caller_name: Optional[str] = Field(None, max_length=255)


class Person(CustomBaseModel):
    tahoeId: Optional[str] = Field(None, max_length=255, alias="tahoe_id")
    first_name: Optional[str] = Field(None, max_length=255)
    middle_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[Date] = None
    age: Optional[int] = None
    is_decedent: Optional[bool] = None
    date_of_death: Optional[Date] = None
    person_type: Optional[str] = Field(
        "Owner", max_length=255, pattern="^(Owner|Relative|Neighbor|Associate)$"
    )
    relationship_to_owner: Optional[str] = Field(None, max_length=255)
    phone_numbers: Optional[List] = []
    emails: Optional[List] = []
    addresses: Optional[list] = []
    date_fields: ClassVar[set[str]] = {"date_of_birth", "date_of_death"}


class Auction(CustomBaseModel):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    date: Optional[Date] = None
    opening_bid: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    current_bid: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    rounding_fields: ClassVar[set[str]] = {"amount", "opening_bid"}
    date_fields: ClassVar[set[str]] = {"date"}


class Sale(CustomBaseModel):
    sale_date: Optional[Date] = None
    sale_amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    current_bid: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    sale_status: Optional[str] = None
    nos_amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    rounding_fields: ClassVar[set[str]] = {"sale_amount", "nos_amount"}
    date_fields: ClassVar[set[str]] = {"sale_date"}


class Debt(CustomBaseModel):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    rounding_fields: ClassVar[set[str]] = {"amount"}


class LegalProceeding(CustomBaseModel):
    trustee_name: Optional[str] = None
    trustee_phone: Optional[str] = None
    trustee_sale_number: Optional[str] = None
    final_judgment: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    plaintiff: Optional[str] = None
    attorney_name: Optional[str] = None
    attorney_phone: Optional[str] = None
    attorney_bar_no: Optional[Union[str, int]] = None
    attorney_firm: Optional[str] = None
    attorney_firm_address: Optional[str] = None
    defendants: Optional[str] = None
    total_amount_owed: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    document_name: Optional[str] = None
    case_number: Optional[str] = None
    case_type: Optional[str] = None
    date_of_filing: Optional[Date] = None
    personal_representative: Optional[str] = None
    probate_case_number: Optional[str] = None
    borrowers_debtors: Optional[str] = None
    lienholders: Optional[str] = None
    rounding_fields: ClassVar[set[str]] = {"final_judgment", "total_amount_owed"}
    date_fields: ClassVar[set[str]] = {"date_of_filing"}


class Mortgage(CustomBaseModel):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    interest_rate: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    late_charge: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    monthly_payment: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    recording_date: Optional[Date] = None
    default_date: Optional[Date] = None
    document_date: Optional[Date] = None
    maturity_date: Optional[Date] = None
    document_number: Optional[str] = Field(None, max_length=255)
    recording_book: Optional[str] = Field(None, max_length=255)
    recording_page: Optional[str] = Field(None, max_length=255)
    lender_name: Optional[str] = Field(None, max_length=255)
    term_type: Optional[str] = Field(None, max_length=255)
    term: Optional[str] = Field(None, max_length=255)
    document_code: Optional[str] = Field(None, max_length=255)
    transaction_type: Optional[str] = Field(None, max_length=255)
    grantee_name: Optional[str] = Field(None, max_length=255)
    riders: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    position: Optional[str] = Field(None, max_length=255)
    term_description: Optional[str] = Field(None, max_length=255)
    loan_type: Optional[str] = Field(None, max_length=255)
    book_and_page: Optional[str] = Field(None, max_length=255)
    rounding_fields: ClassVar[set[str]] = {"amount", "interest_rate", "late_charge"}
    date_fields: ClassVar[set[str]] = {
        "recording_date",
        "default_date",
        "document_date",
        "maturity_date",
    }


class Loan(CustomBaseModel):
    id: Optional[str] = Field(None, max_length=255)
    recording_date: Optional[Date] = None
    sale_date: Optional[Date] = None
    monthly_payment: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    loan_recording_date: Optional[Date] = None
    loan_due_date: Optional[Date] = None
    loan_term: Optional[int] = None
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    loan_interest_rate: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    estimated_loan_payment: Optional[Decimal] = Field(
        None, max_digits=12, decimal_places=2
    )
    estimated_loan_balance: Optional[Decimal] = Field(
        None, max_digits=12, decimal_places=2
    )
    document_number: Optional[str] = Field(None, max_length=255)
    document_type: Optional[str] = Field(None, max_length=255)
    transaction_type: Optional[str] = Field(None, max_length=255)
    loan_type: Optional[str] = Field(None, max_length=255)
    financing_type: Optional[str] = Field(None, max_length=255)
    buyer_names: Optional[str] = Field(None, max_length=255)
    loan_detail: Optional[str] = Field(None, max_length=255)
    purchase_method: Optional[str] = Field(None, max_length=255)
    lender_name: Optional[str] = Field(None, max_length=255)
    amount_estimated: Optional[bool] = None
    book_and_page: Optional[str] = Field(None, max_length=255)

    rounding_fields: ClassVar[set[str]] = {
        "amount",
        "estimated_loan_payment",
        "estimated_loan_balance",
        "loan_interest_rate",
    }
    date_fields: ClassVar[set[str]] = {
        "recording_date",
        "sale_date",
        "loan_recording_date",
        "loan_due_date",
    }


class Transaction(CustomBaseModel):
    id: Optional[int] = None
    recording_date: Optional[Date] = None
    sale_date: Optional[Date] = None
    loan_recording_date: Optional[Date] = None
    loan_due_date: Optional[Date] = None
    loan_term: Optional[int] = None
    amount: Optional[Decimal] = Field(0, max_digits=12, decimal_places=2)
    loan_interest_rate: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    loan_type: Optional[str] = None
    document_number: Optional[str] = None
    document_type: Optional[str] = None
    transaction_type: Optional[str] = None
    financingType: Optional[str] = None
    buyer_names: Optional[str] = None
    seller_names: Optional[str] = None
    purchase_method: Optional[str] = None
    lender_name: Optional[str] = None
    rounding_fields: ClassVar[set[str]] = {"amount", "loan_interest_rate"}
    date_fields: ClassVar[set[str]] = {
        "recording_date",
        "sale_date",
        "loan_recording_date",
        "loan_due_date",
    }


class Foreclosure(CustomBaseModel):
    id: Optional[int] = None
    type: Optional[str] = Field(None, max_length=255)
    recording_date: Optional[Date] = None
    default_date: Optional[Date] = None
    original_recording_date: Optional[Date] = None
    original_document_date: Optional[Date] = None
    listing_date: Optional[Date] = None
    document_number: Optional[str] = Field(None, max_length=255)
    recording_book: Optional[str] = Field(None, max_length=255)
    recording_page: Optional[str] = Field(None, max_length=255)
    document_type: Optional[str] = Field(None, max_length=255)
    case_number: Optional[str] = Field(None, max_length=255)
    original_document_number: Optional[str] = Field(None, max_length=255)
    original_recording_book: Optional[str] = Field(None, max_length=255)
    original_recording_page: Optional[str] = Field(None, max_length=255)
    trustee_last_name: Optional[str] = Field(None, max_length=255)
    borrower1_company: Optional[str] = Field(None, max_length=255)
    borrower2_company: Optional[str] = Field(None, max_length=255)
    report_description: Optional[str] = None
    recording_book_page: Optional[str] = Field(None, max_length=255)
    original_recording_book_page: Optional[str] = Field(None, max_length=255)
    borrower1_name: Optional[str] = Field(None, max_length=255)
    borrower2_name: Optional[str] = Field(None, max_length=255)
    borrower_names: Optional[str] = None
    trustee_name: Optional[str] = Field(None, max_length=255)
    type_name: Optional[str] = Field(None, max_length=255)
    active: Optional[bool] = Field(default=None)
    date_fields: ClassVar[set[str]] = {
        "recording_date",
        "default_date",
        "original_recording_date",
        "original_document_date",
        "listing_date",
    }


class Lien(CustomBaseModel):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    listing_amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    listing_date: Optional[Date] = None
    recording_date: Optional[Date] = None
    tax_date: Optional[Date] = None
    tax_period_min: Optional[Date] = None
    tax_period_max: Optional[Date] = None
    fips: Optional[str] = Field(None, max_length=255)
    apn_unformatted: Optional[str] = Field(None, max_length=255)
    block: Optional[str] = Field(None, max_length=255)
    range: Optional[str] = Field(None, max_length=255)
    township: Optional[str] = Field(None, max_length=255)
    district: Optional[str] = Field(None, max_length=255)
    district_suffix: Optional[str] = Field(None, max_length=255)
    land_lot: Optional[str] = Field(None, max_length=255)
    lot_number: Optional[str] = Field(None, max_length=255)
    damar_document_code: Optional[str] = Field(None, max_length=255)
    document_type: Optional[str] = Field(None, max_length=255)
    document_number: Optional[str] = Field(None, max_length=255)
    recording_book: Optional[str] = Field(None, max_length=255)
    recording_page: Optional[str] = Field(None, max_length=255)
    tax_type: Optional[str] = Field(None, max_length=255)
    tax_number: Optional[str] = Field(None, max_length=255)
    creditor_name: Optional[str] = Field(None, max_length=255)
    stay_ordered: Optional[bool] = Field(default=None)
    installment_judgment: Optional[bool] = Field(default=None)
    assignee_of_record: Optional[bool] = Field(default=None)
    additional_judgment_debtors: Optional[bool] = Field(default=None)
    judgment_creditor: Optional[bool] = Field(default=None)
    bankruptcy_asset: Optional[bool] = Field(default=None)
    bankruptcy_pro_se: Optional[bool] = Field(default=None)
    type: Optional[str] = Field(None, max_length=255)
    effective_debtor_names: Optional[str] = Field(None, max_length=255)
    effective_petitioner_names: Optional[str] = Field(None, max_length=255)
    debtor_name: Optional[str] = Field(None, max_length=255)
    type_description: Optional[str] = Field(None, max_length=255)
    recording_book_page: Optional[str] = Field(None, max_length=255)
    tax_lien: Optional[str] = Field(None, max_length=255)
    date_fields: ClassVar[set[str]] = {
        "recording_date",
        "listing_date",
        "loan_recording_date",
        "tax_date",
        "tax_period_min",
        "tax_period_max",
    }


class Property(CustomBaseModel):
    address: str
    is_auction: bool
    is_obit: bool
    source_name: str
    property_type: Optional[str] = None
    owner_occupied: Optional[bool] = None
    vacant: Optional[bool] = None
    occupancy: Optional[str] = None
    lattitude: Optional[float] = None
    longitude: Optional[float] = None
    mailing_address: Optional[str] = None
    mailing_city: Optional[str] = None
    mailing_state: Optional[str] = None
    mailing_zip: Optional[str] = None
    est_remaining_balance: Optional[Union[float, int]] = None
    zestimate: Optional[Union[float, int]] = None
    zestimate_low: Optional[Union[float, int]] = None
    beds: Optional[int] = None
    baths: Optional[float] = None
    square_footage: Optional[int] = None
    year_built: Optional[int] = None
    status: Optional[str] = None
    link: Optional[str] = None
    county: Optional[str] = None
    auctions: List[Auction] = []
    debts: List[Debt] = []
    sales: List[Sale] = []
    legal_proceedings: List[LegalProceeding] = []
    loans: List[Loan] = []
    mortgages: List[Mortgage] = []
    transactions: List[Transaction] = []
    foreclosures: List[Foreclosure] = []
    liens: List[Lien] = []
    debts: List[Debt] = []
    related_people: List[Person] = []


class Lead(CustomBaseModel):
    link: Optional[str] = None
    stage: Optional[str] = None
    status: Optional[str] = None
    deal_strength: Optional[str] = None
    lead_type: Optional[str] = None
    force: Optional[bool] = False
    assigned_to: Optional[list] = []
    comments: Optional[list] = []
    property: Property
