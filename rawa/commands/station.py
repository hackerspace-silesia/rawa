from typing import Optional

from rawa.models import Station


def find_station(station_id: int) -> Optional[Station]:
    return Station.query.filter_by(id=station_id).first()
