from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.update_vendor_response_vendor_type import UpdateVendorResponseVendorType
import datetime
from ..models.update_vendor_response_subscriptions_list import (
    UpdateVendorResponseSubscriptionsList,
)
from ..models.update_vendor_response_custom_form import UpdateVendorResponseCustomForm
from ..models.update_vendor_response_addressbook_list import (
    UpdateVendorResponseAddressbookList,
)
from ..models.update_vendor_response_currency_list import (
    UpdateVendorResponseCurrencyList,
)
from ..models.update_vendor_response_global_subscription_status import (
    UpdateVendorResponseGlobalSubscriptionStatus,
)
from ..models.update_vendor_response_email_preference import (
    UpdateVendorResponseEmailPreference,
)
from ..models.update_vendor_response_subsidiary import UpdateVendorResponseSubsidiary
from ..models.update_vendor_response_currency import UpdateVendorResponseCurrency


class UpdateVendorResponse(BaseModel):
    """
    Attributes:
        eligible_for_commission (Optional[str]): The Eligible for commission
        unbilled_orders_primary (Optional[int]): The Unbilled orders primary Example: 0.0.
        company_name (Optional[str]): The Company name Example: tstCustomerLeustean updated.
        is_person (Optional[bool]): The Is person
        legal_name (Optional[str]): The Legal name Example: tstCustomerLeustean checking.
        password (Optional[str]): The Password
        balance (Optional[str]): The Balance
        terms (Optional[str]): The Terms
        alt_email (Optional[str]): The Alt email
        fax (Optional[str]): The Fax
        pricing_schedule_list (Optional[str]): The Pricing schedule list
        addressbook_list (Optional[UpdateVendorResponseAddressbookList]):
        give_access (Optional[str]): The Give access
        currency (Optional[UpdateVendorResponseCurrency]):
        vat_reg_number (Optional[str]): The Vat reg number
        representing_subsidiary (Optional[str]): The Representing subsidiary
        work_calendar (Optional[str]): The Work calendar
        mobile_phone (Optional[str]): The Mobile phone
        phone (Optional[str]): The Phone Example: +19999.
        fax_transactions (Optional[bool]): The Fax transactions
        labor_cost (Optional[str]): The Labor cost
        payables_account (Optional[str]): The Payables account
        default_tax_reg (Optional[str]): The Default tax reg
        null_field_list (Optional[str]): The Null field list
        tax_registration_list (Optional[str]): The Tax registration list
        last_name (Optional[str]): The Last name Example: ChurrosLastN2.
        bcn (Optional[str]): The Bcn
        receipt_amount (Optional[str]): The Receipt amount
        bill_pay (Optional[str]): The Bill pay
        currency_list (Optional[UpdateVendorResponseCurrencyList]):
        password2 (Optional[str]): The Password 2
        require_pwd_change (Optional[str]): The Require pwd change
        email (Optional[str]): The Email Example: bogdan.leustean@yahoo.com.
        purchase_order_quantity (Optional[str]): The Purchase order quantity
        purchase_order_amount (Optional[str]): The Purchase order amount
        account_number (Optional[str]): The Account number
        subsidiary (Optional[UpdateVendorResponseSubsidiary]):
        url (Optional[str]): The Url Example: https://wwe.com.
        print_on_check_as (Optional[str]): The Print on check as
        is_job_resource_vend (Optional[bool]): The Is job resource vend
        default_address (Optional[str]): The Default address Example: tstCustomerLeustean updated
            bimili
            Gajuvaka
            Vizag AP 503494
            United States.
        is_inactive (Optional[bool]): The Is inactive
        is_1099_eligible (Optional[bool]): The Is 1099 eligible
        internal_id (Optional[str]): The Internal ID Example: 731211.
        subscriptions_list (Optional[UpdateVendorResponseSubscriptionsList]):
        global_subscription_status (Optional[UpdateVendorResponseGlobalSubscriptionStatus]):
        print_transactions (Optional[bool]): The Print transactions
        credit_limit (Optional[str]): The Credit limit
        custom_form (Optional[UpdateVendorResponseCustomForm]):
        opening_balance (Optional[str]): The Opening balance
        opening_balance_date (Optional[str]): The Opening balance date
        image (Optional[str]): The Image
        home_phone (Optional[str]): The Home phone
        first_name (Optional[str]): The First name Example: ChurrosFirstN.
        receipt_quantity_diff (Optional[str]): The Receipt quantity diff
        incoterm (Optional[str]): The Incoterm
        alt_phone (Optional[str]): The Alt phone
        expense_account (Optional[str]): The Expense account
        salutation (Optional[str]): The Salutation Example: Mr.
        tax_id_num (Optional[str]): The Tax ID num
        phonetic_name (Optional[str]): The Phonetic name
        receipt_quantity (Optional[str]): The Receipt quantity
        tax_item (Optional[str]): The Tax item
        title (Optional[str]): The Title
        send_email (Optional[str]): The Send email
        date_created (Optional[datetime.datetime]): The Date created Example: 2024-05-09T16:33:01.0000000+05:30.
        purchase_order_quantity_diff (Optional[str]): The Purchase order quantity diff
        email_transactions (Optional[bool]): The Email transactions
        opening_balance_account (Optional[str]): The Opening balance account
        unbilled_orders (Optional[str]): The Unbilled orders
        alt_name (Optional[str]): The Alt name
        comments (Optional[str]): The Comments
        last_modified_date (Optional[datetime.datetime]): The Last modified date Example:
            2024-05-09T16:34:17.0000000+05:30.
        email_preference (Optional[UpdateVendorResponseEmailPreference]):
        external_id (Optional[str]): The External ID
        entity_id (Optional[str]): The Entity ID Example: tstCustomerLeustean checking.
        is_accountant (Optional[str]): The Is accountant
        roles_list (Optional[str]): The Roles list
        middle_name (Optional[str]): The Middle name Example: ab.
        category (Optional[str]): The Category
        balance_primary (Optional[int]): The Balance primary Example: 0.0.
        vendor_type (Optional[UpdateVendorResponseVendorType]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    eligible_for_commission: Optional[str] = Field(
        alias="eligibleForCommission", default=None
    )
    unbilled_orders_primary: Optional[int] = Field(
        alias="unbilledOrdersPrimary", default=None
    )
    company_name: Optional[str] = Field(alias="companyName", default=None)
    is_person: Optional[bool] = Field(alias="isPerson", default=None)
    legal_name: Optional[str] = Field(alias="legalName", default=None)
    password: Optional[str] = Field(alias="password", default=None)
    balance: Optional[str] = Field(alias="balance", default=None)
    terms: Optional[str] = Field(alias="terms", default=None)
    alt_email: Optional[str] = Field(alias="altEmail", default=None)
    fax: Optional[str] = Field(alias="fax", default=None)
    pricing_schedule_list: Optional[str] = Field(
        alias="pricingScheduleList", default=None
    )
    addressbook_list: Optional["UpdateVendorResponseAddressbookList"] = Field(
        alias="addressbookList", default=None
    )
    give_access: Optional[str] = Field(alias="giveAccess", default=None)
    currency: Optional["UpdateVendorResponseCurrency"] = Field(
        alias="currency", default=None
    )
    vat_reg_number: Optional[str] = Field(alias="vatRegNumber", default=None)
    representing_subsidiary: Optional[str] = Field(
        alias="representingSubsidiary", default=None
    )
    work_calendar: Optional[str] = Field(alias="workCalendar", default=None)
    mobile_phone: Optional[str] = Field(alias="mobilePhone", default=None)
    phone: Optional[str] = Field(alias="phone", default=None)
    fax_transactions: Optional[bool] = Field(alias="faxTransactions", default=None)
    labor_cost: Optional[str] = Field(alias="laborCost", default=None)
    payables_account: Optional[str] = Field(alias="payablesAccount", default=None)
    default_tax_reg: Optional[str] = Field(alias="defaultTaxReg", default=None)
    null_field_list: Optional[str] = Field(alias="nullFieldList", default=None)
    tax_registration_list: Optional[str] = Field(
        alias="taxRegistrationList", default=None
    )
    last_name: Optional[str] = Field(alias="lastName", default=None)
    bcn: Optional[str] = Field(alias="bcn", default=None)
    receipt_amount: Optional[str] = Field(alias="receiptAmount", default=None)
    bill_pay: Optional[str] = Field(alias="billPay", default=None)
    currency_list: Optional["UpdateVendorResponseCurrencyList"] = Field(
        alias="currencyList", default=None
    )
    password2: Optional[str] = Field(alias="password2", default=None)
    require_pwd_change: Optional[str] = Field(alias="requirePwdChange", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    purchase_order_quantity: Optional[str] = Field(
        alias="purchaseOrderQuantity", default=None
    )
    purchase_order_amount: Optional[str] = Field(
        alias="purchaseOrderAmount", default=None
    )
    account_number: Optional[str] = Field(alias="accountNumber", default=None)
    subsidiary: Optional["UpdateVendorResponseSubsidiary"] = Field(
        alias="subsidiary", default=None
    )
    url: Optional[str] = Field(alias="url", default=None)
    print_on_check_as: Optional[str] = Field(alias="printOnCheckAs", default=None)
    is_job_resource_vend: Optional[bool] = Field(
        alias="isJobResourceVend", default=None
    )
    default_address: Optional[str] = Field(alias="defaultAddress", default=None)
    is_inactive: Optional[bool] = Field(alias="isInactive", default=None)
    is_1099_eligible: Optional[bool] = Field(alias="is1099Eligible", default=None)
    internal_id: Optional[str] = Field(alias="internalId", default=None)
    subscriptions_list: Optional["UpdateVendorResponseSubscriptionsList"] = Field(
        alias="subscriptionsList", default=None
    )
    global_subscription_status: Optional[
        "UpdateVendorResponseGlobalSubscriptionStatus"
    ] = Field(alias="globalSubscriptionStatus", default=None)
    print_transactions: Optional[bool] = Field(alias="printTransactions", default=None)
    credit_limit: Optional[str] = Field(alias="creditLimit", default=None)
    custom_form: Optional["UpdateVendorResponseCustomForm"] = Field(
        alias="customForm", default=None
    )
    opening_balance: Optional[str] = Field(alias="openingBalance", default=None)
    opening_balance_date: Optional[str] = Field(
        alias="openingBalanceDate", default=None
    )
    image: Optional[str] = Field(alias="image", default=None)
    home_phone: Optional[str] = Field(alias="homePhone", default=None)
    first_name: Optional[str] = Field(alias="firstName", default=None)
    receipt_quantity_diff: Optional[str] = Field(
        alias="receiptQuantityDiff", default=None
    )
    incoterm: Optional[str] = Field(alias="incoterm", default=None)
    alt_phone: Optional[str] = Field(alias="altPhone", default=None)
    expense_account: Optional[str] = Field(alias="expenseAccount", default=None)
    salutation: Optional[str] = Field(alias="salutation", default=None)
    tax_id_num: Optional[str] = Field(alias="taxIdNum", default=None)
    phonetic_name: Optional[str] = Field(alias="phoneticName", default=None)
    receipt_quantity: Optional[str] = Field(alias="receiptQuantity", default=None)
    tax_item: Optional[str] = Field(alias="taxItem", default=None)
    title: Optional[str] = Field(alias="title", default=None)
    send_email: Optional[str] = Field(alias="sendEmail", default=None)
    date_created: Optional[datetime.datetime] = Field(alias="dateCreated", default=None)
    purchase_order_quantity_diff: Optional[str] = Field(
        alias="purchaseOrderQuantityDiff", default=None
    )
    email_transactions: Optional[bool] = Field(alias="emailTransactions", default=None)
    opening_balance_account: Optional[str] = Field(
        alias="openingBalanceAccount", default=None
    )
    unbilled_orders: Optional[str] = Field(alias="unbilledOrders", default=None)
    alt_name: Optional[str] = Field(alias="altName", default=None)
    comments: Optional[str] = Field(alias="comments", default=None)
    last_modified_date: Optional[datetime.datetime] = Field(
        alias="lastModifiedDate", default=None
    )
    email_preference: Optional["UpdateVendorResponseEmailPreference"] = Field(
        alias="emailPreference", default=None
    )
    external_id: Optional[str] = Field(alias="externalId", default=None)
    entity_id: Optional[str] = Field(alias="entityId", default=None)
    is_accountant: Optional[str] = Field(alias="isAccountant", default=None)
    roles_list: Optional[str] = Field(alias="rolesList", default=None)
    middle_name: Optional[str] = Field(alias="middleName", default=None)
    category: Optional[str] = Field(alias="category", default=None)
    balance_primary: Optional[int] = Field(alias="balancePrimary", default=None)
    vendor_type: Optional[UpdateVendorResponseVendorType] = Field(
        alias="vendorType", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["UpdateVendorResponse"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
