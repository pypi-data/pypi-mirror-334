from .base import BaseModel

class InvoiceUploaded(BaseModel):

    def __init__(
        self,
        uuid=None,
        amount_of_pages=None
    ):
            
        super().__init__()

        self.uuid = uuid
        self.amount_of_pages = amount_of_pages