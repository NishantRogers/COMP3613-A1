# CLI Commands

Initializes the database and populates it.
```
flask init
```

## Staff Commands

Create a new staff member.
```
flask staff create <name> <password>
Example: flask staff create tom tompass
```

View the full roster for this week.
```
flask staff roster
```

Clock staff in or out of a shift.
```
flask staff clock <in|out> <shiftId>
Example: flask staff clock in 4
```

## Admin Commands

Create a new admin.
```
flask admin create <name> <password>
Example: flask admin create john johnpass
```

Schedule a shift.
```
flask admin schedule <staffId> <adminId> <startTime> <endTime>
Example: flask admin schedule 1 1 "26/09/2025 09:00" "26/09/2025 17:00"
```

List all reports.
```
flask admin reports
```

Create a new report.
```
flask admin create_report
```

View a report by ID.
```
flask admin report <reportId>
Example: flask admin report 2
```
