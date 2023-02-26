class Booking:
    def __init__(
        self,
        experience_id: str,
        reserver_id: str,
        owner_id: str,
        date: str,
        id: str,
        amount: int,
        guests: int,
    ):
        self.experience_id = experience_id
        self.reserver_id = reserver_id
        self.owner_id = owner_id
        self.date = date
        self.id = id
        self.amount = amount
        self.guests = guests
