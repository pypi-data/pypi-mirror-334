from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime
from ..models.create_vendor_response_currency_list import (
    CreateVendorResponseCurrencyList,
)
from ..models.create_vendor_response_global_subscription_status import (
    CreateVendorResponseGlobalSubscriptionStatus,
)
from ..models.create_vendor_response_address_2 import CreateVendorResponseAddress2
from ..models.create_vendor_response_currency import CreateVendorResponseCurrency
from ..models.create_vendor_response_email_preference import (
    CreateVendorResponseEmailPreference,
)
from ..models.create_vendor_response_address_1 import CreateVendorResponseAddress1
from ..models.create_vendor_response_subscriptions_list import (
    CreateVendorResponseSubscriptionsList,
)
from ..models.create_vendor_response_custom_form import CreateVendorResponseCustomForm
from ..models.create_vendor_response_subsidiary import CreateVendorResponseSubsidiary


class CreateVendorResponse(BaseModel):
    """
    Attributes:
        address1 (Optional[CreateVendorResponseAddress1]):
        unbilled_orders_primary (Optional[int]): The Unbilled orders primary Example: 0.0.
        company_name (Optional[str]): The Company name Example: tstCustomerLeustean updated.
        is_person (Optional[bool]): The Is person
        legal_name (Optional[str]): The Legal name Example: tstCustomerLeustean checking.
        currency (Optional[CreateVendorResponseCurrency]):
        address2 (Optional[CreateVendorResponseAddress2]):
        phone (Optional[str]): The Phone Example: +19999.
        fax_transactions (Optional[bool]): The Fax transactions
        last_name (Optional[str]): The Last name Example: ChurrosLastN2.
        currency_list (Optional[CreateVendorResponseCurrencyList]):
        email (Optional[str]): The Email Example: bogdan.leustean@yahoo.com.
        subsidiary (Optional[CreateVendorResponseSubsidiary]):
        is_job_resource_vend (Optional[bool]): The Is job resource vend
        is_inactive (Optional[bool]): The Is inactive
        is_1099_eligible (Optional[bool]): The Is 1099 eligible
        internal_id (Optional[str]): The Internal ID Example: 731211.
        subscriptions_list (Optional[CreateVendorResponseSubscriptionsList]):
        global_subscription_status (Optional[CreateVendorResponseGlobalSubscriptionStatus]):
        print_transactions (Optional[bool]): The Print transactions
        custom_form (Optional[CreateVendorResponseCustomForm]):
        first_name (Optional[str]): The First name Example: ChurrosFirstN.
        salutation (Optional[str]): The Salutation Example: Mr.
        date_created (Optional[datetime.datetime]): The Date created Example: 2024-05-09T16:33:01.0000000+05:30.
        email_transactions (Optional[bool]): The Email transactions
        last_modified_date (Optional[datetime.datetime]): The Last modified date Example:
            2024-05-09T16:34:17.0000000+05:30.
        email_preference (Optional[CreateVendorResponseEmailPreference]):
        entity_id (Optional[str]): The Entity ID Example: tstCustomerLeustean checking.
        middle_name (Optional[str]): The Middle name Example: ab.
        balance_primary (Optional[int]): The Balance primary Example: 0.0.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address1: Optional["CreateVendorResponseAddress1"] = Field(
        alias="address1", default=None
    )
    unbilled_orders_primary: Optional[int] = Field(
        alias="unbilledOrdersPrimary", default=None
    )
    company_name: Optional[str] = Field(alias="companyName", default=None)
    is_person: Optional[bool] = Field(alias="isPerson", default=None)
    legal_name: Optional[str] = Field(alias="legalName", default=None)
    currency: Optional["CreateVendorResponseCurrency"] = Field(
        alias="currency", default=None
    )
    address2: Optional["CreateVendorResponseAddress2"] = Field(
        alias="address2", default=None
    )
    phone: Optional[str] = Field(alias="phone", default=None)
    fax_transactions: Optional[bool] = Field(alias="faxTransactions", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    currency_list: Optional["CreateVendorResponseCurrencyList"] = Field(
        alias="currencyList", default=None
    )
    email: Optional[str] = Field(alias="email", default=None)
    subsidiary: Optional["CreateVendorResponseSubsidiary"] = Field(
        alias="subsidiary", default=None
    )
    is_job_resource_vend: Optional[bool] = Field(
        alias="isJobResourceVend", default=None
    )
    is_inactive: Optional[bool] = Field(alias="isInactive", default=None)
    is_1099_eligible: Optional[bool] = Field(alias="is1099Eligible", default=None)
    internal_id: Optional[str] = Field(alias="internalId", default=None)
    subscriptions_list: Optional["CreateVendorResponseSubscriptionsList"] = Field(
        alias="subscriptionsList", default=None
    )
    global_subscription_status: Optional[
        "CreateVendorResponseGlobalSubscriptionStatus"
    ] = Field(alias="globalSubscriptionStatus", default=None)
    print_transactions: Optional[bool] = Field(alias="printTransactions", default=None)
    custom_form: Optional["CreateVendorResponseCustomForm"] = Field(
        alias="customForm", default=None
    )
    first_name: Optional[str] = Field(alias="firstName", default=None)
    salutation: Optional[str] = Field(alias="salutation", default=None)
    date_created: Optional[datetime.datetime] = Field(alias="dateCreated", default=None)
    email_transactions: Optional[bool] = Field(alias="emailTransactions", default=None)
    last_modified_date: Optional[datetime.datetime] = Field(
        alias="lastModifiedDate", default=None
    )
    email_preference: Optional["CreateVendorResponseEmailPreference"] = Field(
        alias="emailPreference", default=None
    )
    entity_id: Optional[str] = Field(alias="entityId", default=None)
    middle_name: Optional[str] = Field(alias="middleName", default=None)
    balance_primary: Optional[int] = Field(alias="balancePrimary", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateVendorResponse"], src_dict: Dict[str, Any]):
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
