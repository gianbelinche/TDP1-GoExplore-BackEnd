class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        id: str,
        password: str,
        birth_date: str,
        cards: list,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = id
        self.password = password
        self.birth_date = birth_date
        self.cards = cards


class Card:
    def __init__(self, number: str, expiry_date: str, security_code: str):
        self.number = number
        self.expiry_date = expiry_date
        self.security_code = security_code

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "security_code": self.security_code,
            "expiry_date": self.expiry_date,
        }
