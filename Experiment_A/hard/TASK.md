# Hard Task: Room Booking System

## Objective
Identify and fix defects in booking.py.

Preserve the existing public class and method names.

## Functional Requirements

1. The system must support multiple bookings.

2. Each booking must have a unique booking ID.

3. Bookings must be stored in a dictionary
   using booking IDs as keys.

4. calculate_time(time) must:
   - Accept valid 24-hour HH:MM times.
   - Convert valid times into minutes.
   - Accept 00:00 through 23:59.
   - Raise ValueError for invalid times or formats.

5. availability(room, day, start_time, end_time):
   - Returns True when the room is available.
   - Returns False when a booking overlaps.
   - Checks conflicts for the same room and day.
   - Allows adjacent bookings.
   - Allows identical times on different days.
   - Allows identical times in different rooms.

6. Booking intervals must:
   - Have a start time earlier than the end time.
   - Reject zero-duration bookings.
   - Reject overnight bookings.
   - Raise ValueError for invalid intervals.

7. book_room(id, room, day, start_time, end_time):
   - Creates a booking when the room is available.
   - Returns True when booking succeeds.
   - Returns False when a time conflict occurs.
   - Rejects duplicate booking IDs with ValueError.
   - Must not overwrite an existing booking.

8. cancel_booking(id):
   - Removes an existing booking.
   - Returns True when cancellation succeeds.
   - Returns False when the booking does not exist.

9. list_bookings(room, day):
   - Returns bookings matching the specified room.
   - Returns bookings matching the specified day.
   - Sorts bookings by starting time.
   - Returns an empty list when no bookings match.

10. Dates must:
    - Follow YYYY-MM-DD format.
    - Represent valid calendar dates.
    - Raise ValueError for invalid dates.

11. Booking IDs and room names must:
    - Be nonempty strings.
    - Raise ValueError for invalid inputs.

12. Each booking must store:
    - id
    - room
    - day
    - start_time
    - end_time

## Constraints

- Preserve class name booking.
- Preserve existing public method names.
- list_bookings may be updated to accept
  room and day parameters.
- Do not modify TASK.md.