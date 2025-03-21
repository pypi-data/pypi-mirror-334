from .base import BaseModel, ObjectListModel

class UserInfo(BaseModel):

    def __init__(self,
        sub=None,
        username=None,
        email=None,
        name=None,
        family_name=None,
        given_name=None,
        locale=None,
        preferred_username=None,
        accountant_id=None,
        accountant_name=None,
        accountant_vat_number=None,
        accountant_features=None,
        type=None
    ):

        super().__init__()

        self.sub = sub
        self.username = username
        self.email = email
        self.name = name
        self.family_name = family_name
        self.given_name = given_name
        self.locale = locale
        self.preferred_username = preferred_username
        self.accountant_id = accountant_id
        self.accountant_name = accountant_name
        self.accountant_vat_number = accountant_vat_number
        self.accountant_features = accountant_features
        self.type = type

class Administration(BaseModel):

    def __init__(self,
        name=None,
        company_number=None,
        emails=None,
        company_type=None,
        address=None,
        account_manager=None
    ):
        super().__init__()

        self.name = name
        self.company_number = company_number
        self.emails = emails if emails else Emails()
        self.company_type = company_type
        self.address = address if address else Address()
        self.account_manager = account_manager

class Administrations(ObjectListModel):
    list_object = Administration

class Email(BaseModel):

    def __init__(self,
        email_type=None,
        email_address=None,
    ):
        super().__init__()

        self.type = email_type
        self.email_address = email_address

class Emails(ObjectListModel):
    list_object = Email

class Address(BaseModel):

    def __init__(self,
        street_address=None,
        country=None,
    ):
        super().__init__()

        self.street_address = street_address
        self.country = country if country else Country()

class Country(BaseModel):

    def __init__(self,
        iso2=None,
        name=None,
    ):
        super().__init__()

        self.iso2 = iso2
        self.name = name