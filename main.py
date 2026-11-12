
from drafter import *
from dataclasses import dataclass
from datetime import datetime
from bakery import assert_equal

#The event dataclass will store the information for a single event.
@dataclass
class Event:
    date: str
    title: str
    description: str


#This will store information about the entire website
@dataclass
class State:
    events: list
    message: str


#This will be the front page of the website. It will essentially be the hub for everything that goes on.
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Calendar"),
        "This is your personal calendar!",
        "Keep track of assignments, meetings, and other events.",
        HorizontalRule(),

        Header("Calendar Menu", 2),

        Button("Add an Event", "add_page"),
        Button("View All Events", "view_all"),
        Button("View Events on a Specific Day", "day_page"),
        Button("Search for an Event", "search_page"),
        Button("Delete an Event", "delete_page"),

        HorizontalRule(),
        "Total Events: " + str(len(state.events)),
        state.message
    ])


#this is the page that adds an event. it will ask about when the date should be
@route
def add_page(state: State) -> Page:
    return Page(state, [
        Header("Add a Event"),

        "Enter the date (YYYY-MM-DD):",
        TextBox("event_date"),

        "Enter the title of that event:",
        TextBox("event_title"),

        "Enter the description:",
        TextArea("event_description"),

        Button("Add Event", "add_event"),
        Button("Return Home", "index")
    ])


#this function will add an event and store it in the general page state.
@route
def add_event(state: State, event_date: str,
              event_title: str,
              event_description: str) -> Page:

    #I have tooken computer science classes in highschool and I do not think we have covered try and except but basically try runs a code and then if an error occurs it will run the except
    try:
        datetime.strptime(event_date, "%Y-%m-%d")

    except ValueError:
        state.message = "Please enter a valid date using YYYY-MM-DD."
        return add_page(state)

    if event_title.strip() == "":
        state.message = "Please enter an event title."
        return add_page(state)

    new_event = Event(
        event_date,
        event_title,
        event_description
    )

    found = False
    i = 0


#This while loop effectively checks if an event already exists. This does not seem neccesary but I ran into some issues with finding and event so I added this in
    while i < len(state.events):

        if (state.events[i].date == event_date and
                state.events[i].title.lower() ==
                event_title.lower()):

            state.events[i] = new_event
            found = True

        i = i + 1

    if found == False:
        state.events.append(new_event)

    state.message = "Event added successfully!"

    return index(state)


#this is the page to view all the events
@route
def view_all(state: State) -> Page:

    contents = [
        Header("All Calendar Events")
    ]

    if len(state.events) == 0:
        contents.append("There is not events yet. You should add one!")

    else:

        # FOR LOOP 1
        for event in state.events:
            contents.append(HorizontalRule())
            contents.append("Date: " + event.date)
            contents.append("Title: " + event.title)
            contents.append("Description: " + event.description)

    contents.append(HorizontalRule())
    contents.append(Button("Return Home", "index"))

    return Page(state, contents)


#this is the page to view a specific event
@route
def day_page(state: State) -> Page:
    return Page(state, [
        Header("View Events by Date"),
        "Enter the day you want to view (YYYY-MM-DD):",
        TextBox("selected_date"),
        Button("Find Events", "view_day"),
        Button("Return Home", "index")
    ])


#view day will let you see a selected day
@route
def view_day(state: State, selected_date: str) -> Page:

    contents = [
        Header("Events for " + selected_date)
    ]

    found = False
    for event in state.events:

        if event.date == selected_date:
            contents.append(HorizontalRule())
            contents.append("Title: " + event.title)
            contents.append("Description: " + event.description)
            found = True

    if found == False:
        contents.append("No events found for this day.")

    contents.append(Button("Return Home", "index"))

    return Page(state, contents)


#this function will search for an event 
@route
def search_page(state: State) -> Page:
    return Page(state, [
        Header("Search Events"),
        "Enter a word or phrase from an event title:",
        TextBox("search_text"),
        Button("Search", "search_event"),
        Button("Return Home", "index")
    ])


#this function will search for an event by asking for the day that it is wanted
@route
def search_event(state: State, search_text: str) -> Page:

    contents = [
        Header("Search Results")
    ]

    found = False

    for event in state.events:

        if search_text.lower() in event.title.lower():
            contents.append(HorizontalRule())
            contents.append("Title: " + event.title)
            contents.append("Date: " + event.date)
            contents.append("Description: " + event.description)
            found = True

    if found == False:
        contents.append("No matching events were found.")

    contents.append(Button("Return Home", "index"))

    return Page(state, contents)


#this function will use a page and delete an event 
@route
def delete_page(state: State) -> Page:

    contents = [
        Header("Delete an Event")
    ]

    if len(state.events) == 0:
        contents.append("There are no events to delete.")

    else:
        contents.append("Enter the exact event title:")
        contents.append(TextBox("delete_title"))

        contents.append("Enter the event date (YYYY-MM-DD):")
        contents.append(TextBox("delete_date"))

        contents.append(Button("Delete Event", "delete_event"))

    contents.append(Button("Return Home", "index"))

    return Page(state, contents)


#this function will delete an event individually
@route
def delete_event(state: State, delete_title: str,
                 delete_date: str) -> Page:

    found = False
    i = 0

    # Search through the events to find the one to delete
    while i < len(state.events):

        if (state.events[i].title.lower() ==
                delete_title.lower() and
                state.events[i].date == delete_date):

            state.events.pop(i)
            found = True
            break

        i = i + 1

    if found == True:
        state.message = "Event deleted successfully!"

    else:
        state.message = "Event could not be found."

    return index(state)


#this is the final code that will start the website
start_server(
    State([], "Welcome to your calendar!"),
    site_title="My Calendar"
)

