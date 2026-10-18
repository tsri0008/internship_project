class booking:
    def __init__(self):
        self.booking = {}

    def calculate_time(self, time): 
        cal_time_hour, cal_time_minute = time.split(":")

        total_minutes = (int(cal_time_hour) * 60) + int(cal_time_minute)

        if total_minutes < 0 or total_minutes >= 1440: 
            raise ValueError("Time must be greater than zero.")

        return total_minutes

    def availability(self, room, day, start_time, end_time):
        # main resposibility of this function is to check whether there's already a room as well as if its occupied for the time they want to book it for.
        # going through all the rooms
        available = True

        for id in self.booking: 
            # if the room matches 
            if self.booking[id]["room"] == room:
                # calculate the time currently assigning to the room
                current_start_time = self.calculate_time(self.booking[id]["start_time"])
                current_end_time = self.calculate_time(self.booking[id]["end_time"])
                start_time = self.calculate_time(start_time)
                end_time = self.calculate_time(end_time)

                # if the starting time and ending time of the same day are within the current booking's starting time and comes before the current booking's ending time.
                if day == self.booking[id]["day"]:
                    if current_start_time <= start_time <= current_end_time:
                        # tell them its occupied
                        available = False
                        return available
                    if current_start_time <= end_time <= current_end_time:
                        # tell them its occupied
                        available = False
                        return available
                        
        # tell them its available
        return available

    def book_room(self, id, room, day, start_time, end_time):
        # check if the room is available for the time they want to book it for.
        if self.availability(room, day, start_time, end_time) == False:
            # if it is available, add it to the booking dictionary
            self.booking[id] = {"id": id, "room": room, "day": day, "start_time": start_time, "end_time": end_time}


    def cancel_booking(self, id):
        for rooms in self.booking:
            if rooms == id:
                del self.booking[id]
                print("Booking cancelled successfully.")
                return True
            else:
                print("No booking found with the given ID.")
                return False

    def list_bookings(self):
        return [booking for booking in self.booking.values()]