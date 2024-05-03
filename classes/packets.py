from pydantic import BaseModel


class Packet(BaseModel):
    packet_id: int

