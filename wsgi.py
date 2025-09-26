import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Staff, Admin, Shift, Report
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize,
    createAdmin, schedule, listAdmins, getAdmin, deleteAdmin,
    createStaff, clockInOut, listStaff, getStaff, deleteStaff,
    getShiftInfo, deleteShift, printShiftInfo,
    createRoster, createReportData, createReport, listReports, printReportInfo, getReport, deleteReport
)

app = create_app()
migrate = get_migrate(app)


'''
Database Init Command
'''
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')


'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)


'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Manage Staff members')

@staff_cli.command("list", help="Show all staff")
def list_staff_command():
    print(listStaff())

@staff_cli.command("roster", help="View the roster for the week")
def view_roster_command():
    roster = createRoster()
    str = 'Weekly Roster:\n'
    for staff in roster:
        str += f'\n{staff}:\n'
        for shift in roster[staff]:
            str += f'  {shift}\n'
    print(str)

@staff_cli.command("create", help="Add a new staff member")
@click.argument('name', default="tempStaff")
@click.argument('password', default="tempStaffpass")
def create_staff_command(name, password):
    staff = createStaff(name, password)
    if not staff:
        print("Could not create staff user")
    else:
        print(f'Staff member {staff.name} created')

@staff_cli.command("clock", help="Clock in/out of a shift")
@click.argument("type", type=click.Choice(["in", "out"], case_sensitive=False))
@click.argument("shiftID", type=int)
def clock_staff_command(type, shiftID):
    string = clockInOut(shiftID, type)
    print(string)

app.cli.add_command(staff_cli)


'''
Admin Commands
'''
admin_cli = AppGroup('admin', help='Manage Admin users')

@admin_cli.command("list", help="Show all admins")
def list_admin_command():
    print(listAdmins())

@admin_cli.command("create", help="Add a new admin")
@click.argument('name', default="tempAdmin")
@click.argument('password', default="tempAdminpass")
def create_admin_command(name, password):
    admin = createAdmin(name, password)
    if not admin:
        print("Could not create admin")
    else:
        print(f'Admin {admin.name} created')

@admin_cli.command("schedule", help='Schedules a shift for a staff user')
@click.argument("staffID", type=int)
@click.argument("adminID", type=int)
@click.argument("startTime")
@click.argument("endTime")
def schedule_shift_command(staffID, adminID, startTime, endTime):
    shift = schedule(staffID, adminID, startTime, endTime)
    if not shift:
        print("Failed to schedule shift")
    else:
        print(f'Shift scheduled successfully.\n {shift.get_json()}')

@admin_cli.command("reports", help="List all reports")
def list_reports_command():
    print(listReports())

@admin_cli.command("create_report", help="Creates a new report")
def create_report_command():
    report = createReport()
    if not report:
        print("Error creating report")
    else:
        print(f'Report created.\n {listreports()}')

@admin_cli.command("report", help="View a report by its ID")
@click.argument("reportID", type=int)
def view_report_command(reportID):
    report = getReport(reportID)
    if not report:
        print("No report found with that ID")
    else:
        print(printReportInfo(report.get_json()))

app.cli.add_command(admin_cli)

'''
Test Commands
'''
test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
