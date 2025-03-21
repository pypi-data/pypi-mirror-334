from pydantic import BaseModel


class Migration(BaseModel):
    def apply(self): ...

    def rollback(self): ...
