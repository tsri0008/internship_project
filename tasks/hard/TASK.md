# Booking System Debugging Task

## Objective

Identify and fix defects in the supplied Python
booking system.

Preserve the existing public class and method names.

## Functional Requirements

1. The system must support multiple bookings.

2. Each booking must have a unique booking ID.

3. A room can have multiple bookings on the same
   day, provided their times do not overlap.

4. Overlapping bookings for the same room and day
   must be rejected.

5. Adjacent bookings must be allowed.

6. Different rooms must be bookable at the same time.

7. The same room must be bookable at the same time
   on different days.

8. Booking times must use valid 24-hour HH:MM format.

9. Start time must be earlier than end time.

10. Dates must be valid and use YYYY-MM-DD format.

11. Room names and booking IDs must be nonempty strings.

12. Invalid inputs must raise ValueError.

13. Creating a booking must return True on success
    and False when rejected due to a time conflict.

14. Cancelling an existing booking must return True.
    Cancelling a nonexistent booking must return False.

15. Listing bookings must return bookings filtered
    by room and date, sorted by starting time.

16. Preserve the existing data structure where
    bookings are stored using booking IDs as keys.