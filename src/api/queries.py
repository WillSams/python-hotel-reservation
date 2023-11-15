from api import DbSession
from api.helpers import is_room_available
from api.models import Reservation, Room

import api.utils as utils


def get_reservation_resolver(obj, info, room_id):
    try:
        db = DbSession()
        reservation = db.query(Reservation).filter_by(room_id=room_id).first()
        payload = {"success": True, "reservation": reservation.to_dict()}
    except AttributeError:
        message = f"Reservation of {room_id} not found"
        utils.log_api_error(__name__, message)
        payload = {
            "success": False,
            "errors": [message],
        }
    return payload


def get_all_reservations_resolver(obj, info):
    try:
        db = DbSession()
        reservations = db.query(Reservation).all()
        reservations = [reservation.to_dict() for reservation in reservations]
        payload = {"success": True, "reservations": reservations}
    except Exception as error:
        messages = [str(error)]
        utils.log_api_error(__name__, messages)
        payload = {"success": False, "errors": messages}
    return payload


def get_available_rooms_resolver(obj, info, input: dict):
    try:
        checkin_date = input.get("checkin_date")
        checkout_date = input.get("checkout_date")

        db = DbSession()
        filter = Room.allow_smoking.is_(True)
        available_rooms = db.query(Room).filter(filter).all()

        filtered_rooms = [
            room
            for room in available_rooms
            if is_room_available(room.id, checkin_date, checkout_date)
        ]

        payload = {"success": True, "rooms": filtered_rooms}
    except Exception as error:
        messages = [str(error)]
        utils.log_api_error(__name__, messages)
        payload = {"success": False, "errors": messages}
    return payload
