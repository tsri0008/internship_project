import re
from datetime import date


class booking:
    def __init__(self):
        self.booking = {}

    @staticmethod
    def _validate_name(value, label):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} must be a nonempty string.")

    @staticmethod
    def _validate_day(day):
        if not isinstance(day, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", day):
            raise ValueError("Date must have YYYY-MM-DD format.")
        try:
            date.fromisoformat(day)
        except ValueError as exc:
            raise ValueError("Date must be a valid calendar date.") from exc

    def calculate_time(self, time):
        if not isinstance(time, str) or not re.fullmatch(r"[0-9]{2}:[0-9]{2}", time):
            raise ValueError("Time must have HH:MM format.")
        hour, minute = map(int, time.split(":"))
        if hour > 23 or minute > 59:
            raise ValueError("Time must be between 00:00 and 23:59.")
        return hour * 60 + minute

    def availability(self, room, day, start_time, end_time):
        self._validate_name(room, "Room")
        self._validate_day(day)
        start = self.calculate_time(start_time)
        end = self.calculate_time(end_time)
        if start >= end:
            raise ValueError("Start time must be earlier than end time.")
        for existing in self.booking.values():
            if existing["room"] == room and existing["day"] == day:
                current_start = self.calculate_time(existing["start_time"])
                current_end = self.calculate_time(existing["end_time"])
                if start < current_end and current_start < end:
                    return False
        return True

    def book_room(self, id, room, day, start_time, end_time):
        self._validate_name(id, "Booking ID")
        if id in self.booking:
            raise ValueError("Booking ID already exists.")
        if not self.availability(room, day, start_time, end_time):
            return False
        self.booking[id] = {
            "id": id, "room": room, "day": day,
            "start_time": start_time, "end_time": end_time,
        }
        return True

    def cancel_booking(self, id):
        self._validate_name(id, "Booking ID")
        if id not in self.booking:
            return False
        del self.booking[id]
        return True

    def list_bookings(self, room, day):
        self._validate_name(room, "Room")
        self._validate_day(day)
        return sorted(
            (entry for entry in self.booking.values()
             if entry["room"] == room and entry["day"] == day),
            key=lambda entry: self.calculate_time(entry["start_time"]),
        )
