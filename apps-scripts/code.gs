var calendars = {
    "Room1": "room1@resource.calendar.google.com",
    "Room2": "room2@resource.calendar.google.com"
}

function storeMultipleCalendarEventsInGCSEvery5minDuringADay() {
    var hours = new Date().getHours();
    if (hours >=8 && hours <= 18) {
        storeMultipleCalendarEventsInGCS()
    } else {
        Logger.log("Skipping caledar data snapshot");
    }
}

function storeMultipleCalendarEventsInGCS() {
    Logger.log("Retrieving data from all calendars");
    for (var key in calendars) {
        if (calendars.hasOwnProperty(key)) {
            storeCalendarEventsInGCS(key, calendars[key]);
        }
    }
}

function storeCalendarEventsInGCS(calendarName, calendarId) {
    var fetch_time = new Date();
    var month = ("0" + (fetch_time.getMonth() + 1)).slice(-2);
    var day = ("0" + fetch_time.getDate()).slice(-2);
    var hours = ("0" + fetch_time.getHours()).slice(-2);
    var minutes = ("0" + fetch_time.getMinutes()).slice(-2);
    var date = fetch_time.getFullYear()+"-"+month+"-"+day;
    var filename = date+"/"+calendarName+"_"+date+"_"+hours+"-"+minutes+".json";

    var midnight = new Date();
    midnight.setHours(0,0,0,0);
    var next7days = new Date(midnight.getTime() + 7 * 24 * 60 * 60 * 1000);
    Logger.log("%s, from: %s, to: %s", filename, midnight.toISOString(), next7days.toISOString());

    events = retrieveEvents(calendarId, midnight, next7days);

    uploadFileToGCS(filename, events);
}

function retrieveEvents(calendarId, from, to) {
    var fields = 'accessRole,description,etag,'+
        'items(anyoneCanAddSelf,attendees,attendeesOmitted,colorId,created,creator,end,endTimeUnspecified,etag,gadget,guestsCanInviteOthers,guestsCanModify,guestsCanSeeOtherGuests,htmlLink,' +
        'iCalUID,id,location,locked,organizer,originalStartTime,privateCopy,recurrence,recurringEventId,sequence,source,start,status,summary,transparency,updated,visibility),' +
        'kind,nextPageToken,nextSyncToken,summary,timeZone,updated';
    var now = new Date();
    var events = Calendar.Events.list(calendarId, {
        timeMin: from.toISOString(),
        timeMax: to.toISOString(),
        singleEvents: true,
        showDeleted: true,
        orderBy: 'startTime',
        maxResults: 500,
        fields: fields
    });
    return events;
}





