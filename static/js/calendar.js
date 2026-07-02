/** Study Sync — FullCalendar integration */

document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("studySyncCalendar");
    if (!calendarEl || typeof FullCalendar === "undefined") return;

    const eventsUrl = window.SS_CALENDAR_EVENTS_URL;
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "timeGridWeek",
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,listWeek",
        },
        height: "auto",
        navLinks: true,
        nowIndicator: true,
        events: eventsUrl,
        eventClick: function (info) {
            const props = info.event.extendedProps;
            alert(
                info.event.title + "\n" +
                "Lecturer: " + props.lecturer + "\n" +
                "Location: " + props.location + "\n" +
                "Spots left: " + props.spots_left
            );
        },
    });

    calendar.render();
});
