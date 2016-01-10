TODO
====

when searching for daily times:
    check for 'daily'
    check for 'weekdays' for weekdays
    check for 'weekends' for weekends
    check for 'holidays' for holidays
        in the absence of a holiday calendar, can force it with a param 

review next_daily_times
    get the tests working again
    eliminate count
    use date param
    use %a values for days
    return query rather than simplified time 

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
