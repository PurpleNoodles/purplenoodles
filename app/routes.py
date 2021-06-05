from flask.templating import render_template
from app import app, config, sqldb
from flask import render_template, redirect, url_for, request, session

@app.route('/')
def home():
    # Create Organization
    sqldb.sql_execute(sqldb.create_account("Microsoft", "microsoft@microsoft.com", "securepass"))
    sqldb.sql_execute(sqldb.create_account("Google", "google@google.com", "googlemypass"))

    # Create Users
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "John", "Smith", "johnsmith@microsoft.com", "smithpass", False))
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "Heather", "Wills", "heatherwills@microsoft.com", "willspass", False))
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "Steve", "West", "stevewest@microsoft.com", "steveypass", False))
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "George", "Jace", "georgejace@microsoft.com", "jacepass", False))
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "Mel", "Move", "melmove@microsoft.com", "melpass", False))
    
    # Create Report
    sqldb.sql_execute(sqldb.create_report("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "9e29f498-2b9f-3c1e-8fd6-fb74a6fd26f8", 50, "This is the report."))

    # Print Organizations
    sqldb.print_table("accounts")
    print()
    # Print Users
    sqldb.print_table("users")
    print()
    # Print Reports
    sqldb.print_table("reports")
    print()

    # Remove User
    sqldb.remove_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "microsoft@microsoft.com", "heatherwills@microsoft.com", "securepass")

    print("\n\n-----------------------------------------------------------------------------------------------------------------------------\n")
    # Print Organizations
    sqldb.print_table("accounts")
    print()
    # Print Users
    sqldb.print_table("users")
    print()
    # Print Reports
    sqldb.print_table("reports")
    print()

    # Remove Organization
    sqldb.remove_account("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "microsoft@microsoft.com", "securepass")

    print("\n\n-----------------------------------------------------------------------------------------------------------------------------\n")
    # Print Organizations
    sqldb.print_table("accounts")
    print()
    # Print Users
    sqldb.print_table("users")
    print()
    # Print Reports
    sqldb.print_table("reports")
    print()

    # Drop tables
    sqldb.sql_execute(sqldb.drop_tables())
    return config

