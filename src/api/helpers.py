from datetime import datetime
from typing import Any, Dict

from sqlalchemy import and_, or_

from api import DbSession
from api.models import Reservation

import api.utils as utils


def is_room_available(
    room_id: int, checkin_date: datetime, checkout_date: datetime
) -> Dict[str, Any]:
    try:
        db = DbSession()
        count = (
            db.query(Reservation)
            .filter(
                and_(
                    Reservation.room_id == room_id,
                    or_(
                        and_(
                            Reservation.checkin_date >= checkin_date,
                            Reservation.checkin_date < checkout_date,
                        ),
                        and_(
                            Reservation.checkout_date > checkin_date,
                            Reservation.checkout_date <= checkout_date,
                        ),
                        and_(
                            Reservation.checkin_date <= checkin_date,
                            Reservation.checkout_date >= checkout_date,
                        ),
                    ),
                )
            )
            .count()
        )

        return {"success": count == 0, "errors": []}
    except Exception as error:
        utils.log_api_error(__name__, [str(error)])
        return {"success": False, "errors": [str(error)]}
