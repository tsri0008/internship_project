class booking:
    def __init__(self):
        self.booking = {}

    def calculate_time(self, time): 
        cal_time_hour, cal_time_minute = time.split(":")

        total_minutes = (int(cal_time_hour) * 60) + int(cal_time_minute)

        if total_minutes < 0: 
            raise ValueError("Time must be greater than zero.")

    def availability(self, room, day, start_time, end_time):
        # main resposibility of this function is to check whether there's already a room as well as if its occupied for the time they want to book it for.
        # going through all the rooms
        for rooms in self.booking: 
            # if the room matches 
            if rooms["room"] == room:
                # calculate the time they want to book for the room
                start_time = calculate_time(start_time)
                end_time = calculate_time(end_time)
                # calculate the time currently assigning to the room
                current_start_time = calculate_time(self.booking[room]["start_time"])
                current_end_time = calculate_time(self.booking[room]["end_time"])


                # if the starting time and ending time of the same day are within the current booking's starting time and comes before the current booking's ending time.
                if day == self.booking[room]["day"]:
                    if current_start_time <= start_time <= current_end_time:
                        if current_start_time <= end_time <= current_end_time:
                            # tell them its occupied
                            return False
                        
                # tell them its available
                return True

    def book_room(self, id, room, day, start_time, end_time):
        # check if the room is available for the time they want to book it for.
        if self.availability(room, day, start_time, end_time):
            # if it is available, add it to the booking dictionary
            self.booking[room] = {"id": id, "room": room, "day": day, "start_time": start_time, "end_time": end_time}
        else:
            print("Room is already booked for the time you want to book it for.")


    def cancel_booking(self, id):
        if id in self.booking:
            del self.booking[id]
            print("Booking cancelled successfully.")
        else:
            print("No booking found with the given ID.")

    def list_bookings(self):
        return [booking for booking in self.booking.values()]
