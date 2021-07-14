from amocrm.v2 import Lead as _Lead, custom_field


class Lead(_Lead):
    name = custom_field.TextCustomField('Name')
    number = custom_field.ContactPhoneField('Phone number')
    email = custom_field.ContactEmailField('Email')
    date = custom_field.DateCustomField("Date of appointment")
    time = custom_field.DateTimeCustomField('Time of appointment')
