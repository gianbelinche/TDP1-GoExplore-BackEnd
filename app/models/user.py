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
