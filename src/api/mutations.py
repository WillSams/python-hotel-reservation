from datetime import datetime
from typing import Any, Dict, cast

from api import DbSession
from api.helpers import is_room_available
from api.models import Reservation

import api.utils as utils


def create_reservation_resolver(obj, info, input: dict) -> Dict[str, Any]:
    room_id = cast(int, input.get("room_id"))
    checkin_date = cast(datetime, input.get("checkin_date"))
    checkout_date = cast(datetime, input.get("checkout_date"))
    total_charge = cast(float, input.get("total_charge"))

    try:
        db = DbSession()
        available = is_room_available(room_id, checkin_date, checkout_date)

        if not available:
            message = "Reservation dates overlap with an existing reservation"
            utils.log_api_error(__name__, message)
            return {
                "success": False,
                "errors": [message],
            }

        reservation = Reservation(
            room_id=room_id,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            total_charge=total_charge,
        )

        db.add(reservation)
        db.commit()

        payload = {"success": True, "reservation": reservation.to_dict()}
    except Exception as error:
        messages = [str(error)]
        utils.log_api_error(__name__, messages)
        payload = {"success": False, "errors": messages}

    return payload
