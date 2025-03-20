from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.update_customer_response_customer_type import (
    UpdateCustomerResponseCustomerType,
)
import datetime
from ..models.update_customer_response_credit_hold_override import (
    UpdateCustomerResponseCreditHoldOverride,
)
from ..models.update_customer_response_parent import UpdateCustomerResponseParent
from ..models.update_customer_response_email_preference import (
    UpdateCustomerResponseEmailPreference,
)
from ..models.update_customer_response_global_subscription_status import (
    UpdateCustomerResponseGlobalSubscriptionStatus,
)
from ..models.update_customer_response_contact_roles_list import (
    UpdateCustomerResponseContactRolesList,
)
from ..models.update_customer_response_addressbook_list import (
    UpdateCustomerResponseAddressbookList,
)
from ..models.update_customer_response_stage import UpdateCustomerResponseStage
from ..models.update_customer_response_receivables_account import (
    UpdateCustomerResponseReceivablesAccount,
)
from ..models.update_customer_response_currency import UpdateCustomerResponseCurrency
from ..models.update_customer_response_alcohol_recipient_type import (
    UpdateCustomerResponseAlcoholRecipientType,
)
from ..models.update_customer_response_subscriptions_list import (
    UpdateCustomerResponseSubscriptionsList,
)
from ..models.update_customer_response_entity_status import (
    UpdateCustomerResponseEntityStatus,
)
from ..models.update_customer_response_access_role import (
    UpdateCustomerResponseAccessRole,
)
from ..models.update_customer_response_subsidiary import (
    UpdateCustomerResponseSubsidiary,
)
from ..models.update_customer_response_custom_form import (
    UpdateCustomerResponseCustomForm,
)
from ..models.update_customer_response_currency_list import (
    UpdateCustomerResponseCurrencyList,
)
from ..models.update_customer_response_language import UpdateCustomerResponseLanguage


class UpdateCustomerResponse(BaseModel):
    """
    Attributes:
        company_name (Optional[str]): The Company name Example: tstCustomerLeustean updated.
        stage (Optional[UpdateCustomerResponseStage]):
        sync_partner_teams (Optional[bool]): The Sync partner teams
        entity_status (Optional[UpdateCustomerResponseEntityStatus]):
        is_person (Optional[bool]): The Is person
        deposit_balance (Optional[int]): The Deposit balance Example: 0.0.
        receivables_account (Optional[UpdateCustomerResponseReceivablesAccount]):
        balance (Optional[int]): The Balance Example: 0.0.
        currency_list (Optional[UpdateCustomerResponseCurrencyList]):
        give_access (Optional[bool]): The Give access
        addressbook_list (Optional[UpdateCustomerResponseAddressbookList]):
        currency (Optional[UpdateCustomerResponseCurrency]):
        taxable (Optional[bool]): The Taxable Example: True.
        alcohol_recipient_type (Optional[UpdateCustomerResponseAlcoholRecipientType]):
        phone (Optional[str]): The Phone Example: +19999.
        fax_transactions (Optional[bool]): The Fax transactions
        web_lead (Optional[str]): The Web lead Example: No.
        last_name (Optional[str]): The Last name Example: fakerfdsfdf.
        overdue_balance (Optional[int]): The Overdue balance Example: 0.0.
        email (Optional[str]): The Email Example: bogdan.leustean@yahoo.com.
        subsidiary (Optional[UpdateCustomerResponseSubsidiary]):
        url (Optional[str]): The Url Example: https://wwe.com.
        ship_complete (Optional[bool]): The Ship complete
        credit_hold_override (Optional[UpdateCustomerResponseCreditHoldOverride]):
        aging (Optional[int]): The Aging Example: 0.0.
        default_address (Optional[str]): The Default address Example: tstCustomerLeustean fdsfsd
            gfgdsfg
            tegf
            vizag Telangana 6365656
            India.
        contact_roles_list (Optional[UpdateCustomerResponseContactRolesList]):
        parent (Optional[UpdateCustomerResponseParent]):
        is_inactive (Optional[bool]): The Is inactive
        internal_id (Optional[str]): Customer ID Example: 730913.
        subscriptions_list (Optional[UpdateCustomerResponseSubscriptionsList]):
        global_subscription_status (Optional[UpdateCustomerResponseGlobalSubscriptionStatus]):
        print_transactions (Optional[bool]): The Print transactions
        custom_form (Optional[UpdateCustomerResponseCustomForm]):
        tax_exempt (Optional[bool]): The Tax exempt
        first_name (Optional[str]): The First name Example: fakervdsd.
        salutation (Optional[str]): The Salutation Example: fakerfdsfsd.
        is_budget_approved (Optional[bool]): The Is budget approved
        access_role (Optional[UpdateCustomerResponseAccessRole]):
        send_email (Optional[bool]): The Send email
        date_created (Optional[datetime.datetime]): The Date created Example: 2024-05-09T11:57:39.0000000+05:30.
        aging2 (Optional[int]): The Aging 2 Example: 0.0.
        aging3 (Optional[int]): The Aging 3 Example: 0.0.
        aging1 (Optional[int]): The Aging 1 Example: 0.0.
        email_transactions (Optional[bool]): The Email transactions
        unbilled_orders (Optional[int]): The Unbilled orders Example: 0.0.
        aging4 (Optional[int]): The Aging 4 Example: 0.0.
        last_modified_date (Optional[datetime.datetime]): The Last modified date Example:
            2024-05-09T12:17:38.0000000+05:30.
        email_preference (Optional[UpdateCustomerResponseEmailPreference]):
        entity_id (Optional[str]): The Entity ID Example: 4582 tstCustomerLeustean fdsfsd.
        language (Optional[UpdateCustomerResponseLanguage]):
        middle_name (Optional[str]): The Middle name Example: fakerfdsfds.
        customer_type (Optional[UpdateCustomerResponseCustomerType]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_name: Optional[str] = Field(alias="companyName", default=None)
    stage: Optional["UpdateCustomerResponseStage"] = Field(alias="stage", default=None)
    sync_partner_teams: Optional[bool] = Field(alias="syncPartnerTeams", default=None)
    entity_status: Optional["UpdateCustomerResponseEntityStatus"] = Field(
        alias="entityStatus", default=None
    )
    is_person: Optional[bool] = Field(alias="isPerson", default=None)
    deposit_balance: Optional[int] = Field(alias="depositBalance", default=None)
    receivables_account: Optional["UpdateCustomerResponseReceivablesAccount"] = Field(
        alias="receivablesAccount", default=None
    )
    balance: Optional[int] = Field(alias="balance", default=None)
    currency_list: Optional["UpdateCustomerResponseCurrencyList"] = Field(
        alias="currencyList", default=None
    )
    give_access: Optional[bool] = Field(alias="giveAccess", default=None)
    addressbook_list: Optional["UpdateCustomerResponseAddressbookList"] = Field(
        alias="addressbookList", default=None
    )
    currency: Optional["UpdateCustomerResponseCurrency"] = Field(
        alias="currency", default=None
    )
    taxable: Optional[bool] = Field(alias="taxable", default=None)
    alcohol_recipient_type: Optional["UpdateCustomerResponseAlcoholRecipientType"] = (
        Field(alias="alcoholRecipientType", default=None)
    )
    phone: Optional[str] = Field(alias="phone", default=None)
    fax_transactions: Optional[bool] = Field(alias="faxTransactions", default=None)
    web_lead: Optional[str] = Field(alias="webLead", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    overdue_balance: Optional[int] = Field(alias="overdueBalance", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    subsidiary: Optional["UpdateCustomerResponseSubsidiary"] = Field(
        alias="subsidiary", default=None
    )
    url: Optional[str] = Field(alias="url", default=None)
    ship_complete: Optional[bool] = Field(alias="shipComplete", default=None)
    credit_hold_override: Optional["UpdateCustomerResponseCreditHoldOverride"] = Field(
        alias="creditHoldOverride", default=None
    )
    aging: Optional[int] = Field(alias="aging", default=None)
    default_address: Optional[str] = Field(alias="defaultAddress", default=None)
    contact_roles_list: Optional["UpdateCustomerResponseContactRolesList"] = Field(
        alias="contactRolesList", default=None
    )
    parent: Optional["UpdateCustomerResponseParent"] = Field(
        alias="parent", default=None
    )
    is_inactive: Optional[bool] = Field(alias="isInactive", default=None)
    internal_id: Optional[str] = Field(alias="internalId", default=None)
    subscriptions_list: Optional["UpdateCustomerResponseSubscriptionsList"] = Field(
        alias="subscriptionsList", default=None
    )
    global_subscription_status: Optional[
        "UpdateCustomerResponseGlobalSubscriptionStatus"
    ] = Field(alias="globalSubscriptionStatus", default=None)
    print_transactions: Optional[bool] = Field(alias="printTransactions", default=None)
    custom_form: Optional["UpdateCustomerResponseCustomForm"] = Field(
        alias="customForm", default=None
    )
    tax_exempt: Optional[bool] = Field(alias="taxExempt", default=None)
    first_name: Optional[str] = Field(alias="firstName", default=None)
    salutation: Optional[str] = Field(alias="salutation", default=None)
    is_budget_approved: Optional[bool] = Field(alias="isBudgetApproved", default=None)
    access_role: Optional["UpdateCustomerResponseAccessRole"] = Field(
        alias="accessRole", default=None
    )
    send_email: Optional[bool] = Field(alias="sendEmail", default=None)
    date_created: Optional[datetime.datetime] = Field(alias="dateCreated", default=None)
    aging2: Optional[int] = Field(alias="aging2", default=None)
    aging3: Optional[int] = Field(alias="aging3", default=None)
    aging1: Optional[int] = Field(alias="aging1", default=None)
    email_transactions: Optional[bool] = Field(alias="emailTransactions", default=None)
    unbilled_orders: Optional[int] = Field(alias="unbilledOrders", default=None)
    aging4: Optional[int] = Field(alias="aging4", default=None)
    last_modified_date: Optional[datetime.datetime] = Field(
        alias="lastModifiedDate", default=None
    )
    email_preference: Optional["UpdateCustomerResponseEmailPreference"] = Field(
        alias="emailPreference", default=None
    )
    entity_id: Optional[str] = Field(alias="entityId", default=None)
    language: Optional["UpdateCustomerResponseLanguage"] = Field(
        alias="language", default=None
    )
    middle_name: Optional[str] = Field(alias="middleName", default=None)
    customer_type: Optional[UpdateCustomerResponseCustomerType] = Field(
        alias="customerType", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["UpdateCustomerResponse"], src_dict: Dict[str, Any]):
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
