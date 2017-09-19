# Fields description https://developers.google.com/google-apps/calendar/v3/reference/events#resource-representations
class Event:
    def __init__(self, event_id, created, status, recurring_event_id, summary, updated, start_date_time, end_date_time, organizer):
        self.event_id = event_id
        self.created = created
        self.status = status
        self.recurring_event_id = recurring_event_id
        self.summary = summary
        self.updated = updated
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.organizer = organizer

    def __repr__(self):
        return "<Event summary:%s status:%s>" % (self.summary, self.status)

    def __str__(self):
        return "<Event summary:%s status:%s>" % (self.summary, self.status)

    def __hash__(self):
        return hash(self.event_id) ^ hash(self.created) ^ hash(self.status) ^ hash(self.recurring_event_id) ^ hash(self.summary) \
               ^ hash(self.start_date_time) ^ hash(self.end_date_time) ^ hash(self.organizer)

    def __eq__(self, other):
        return self.event_id == other.event_id \
               and self.created == other.created \
               and self.status == other.status \
               and self.recurring_event_id == other.recurring_event_id \
               and self.summary == other.summary \
               and self.start_date_time == other.start_date_time \
               and self.end_date_time == other.end_date_time \
               and self.organizer == other.organizer
