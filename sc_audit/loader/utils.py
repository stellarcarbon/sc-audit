from __future__ import annotations
import base64
import datetime

from pydantic import BaseModel

def parse_iso_date(iso_date: str) -> datetime.date:
    return datetime.datetime.fromisoformat(iso_date).date()

def parse_iso_datetime(iso_datetime: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(iso_datetime)

def decode_hash_memo(b64_hash_memo: str) -> str:
    return base64.b64decode(b64_hash_memo).hex()


class VcsSerialNumber(BaseModel):
    batch_number: int
    block_start: int
    block_end: int
    program_code: str | None
    credit_type: str
    vvb_id: str
    registry: str
    country: str
    project_type: int
    project_id: int
    vintage_start: str
    vintage_end: str
    additional_certification: bool

    @classmethod
    def from_str(cls, vcs_serial_number: str) -> VcsSerialNumber:
        split_serial = vcs_serial_number.split('-')
        if len(split_serial) == 12:
            split_serial = [*split_serial[:3], None, *split_serial[3:]]
        
        kwargs = dict(zip(VcsSerialNumber.model_fields, split_serial))
        return VcsSerialNumber(**kwargs) # type: ignore
    
    def to_str(self) -> str:
        serial_dict = self.model_dump()
        if self.program_code is None:
            del serial_dict['program_code']

        serial_dict['additional_certification'] = int(self.additional_certification)
        return '-'.join(map(str, serial_dict.values()))
    
    @property
    def vintage_start_date(self) -> datetime.date:
        return datetime.datetime.strptime(self.vintage_start, "%d%m%Y").date()
    
    @property
    def vintage_end_date(self) -> datetime.date:
        return datetime.datetime.strptime(self.vintage_end, "%d%m%Y").date()
