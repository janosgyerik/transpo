TODO
====

/api/v1/station/:id/times?
  date=      # means "now"
  date=date  # extract time; extract weekday
  time=time  # use time; take current weekday

create form to validate -> tdd
    see how djinn validated form params

if valid, apply filters
    try to use sql filters, not python

tdd getting times for specified date
tdd getting times for specified time (same schedule every day)

create dummy plain text view
create dummy html view

create location

deploy and test from phone

create command to import from simple file (not scraping)
    manually enter from latest schedule


old
---

- base library with cli commands
    - print lines
    - create line
    - create station for line
    - replace timetable for line + station
    - import timetable file of line + station
    - import timetable files of line

- REST API
    - /api/v1/lines/:id
    - /api/v1/lines/:id/stations/:id
    - /api/v1/lines/:id/stations/:id/?from=&to=
    - /api/v1/countries/:id/regions/:id/cities/:id/

- interactive docs
    - /docs/v1/lines/
    - /docs/v1/countries/
