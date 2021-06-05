from flask.templating import render_template
from app import app, config, sqldb, nlp
from flask import render_template, redirect, url_for, request, session

@app.route('/')
def home():
    
    return config


def test_sqldb():
    # Create Organizations
    sqldb.sql_execute(sqldb.create_account("Microsoft", "microsoft@microsoft.com", "securepass"))
    sqldb.sql_execute(sqldb.create_account("Google", "google@google.com", "googlemypass"))
    sqldb.sql_execute(sqldb.create_account("IBM", "ibm@ibm.com", "ibmquantum"))
    sqldb.sql_execute(sqldb.create_account("Oracle", "oracle@oracle.com", "thejavalang"))
    sqldb.sql_execute(sqldb.create_account("MLH", "mlh@mlh.com", "hackingnow"))

    # Create Users
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "John", "Smith", "johnsmith@microsoft.com", "smithpass", False))
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "Heather", "Wills", "heatherwills@microsoft.com", "willspass", False))
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "Steve", "West", "stevewest@microsoft.com", "steveypass", False))
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "George", "Jace", "georgejace@microsoft.com", "jacepass", False))
    sqldb.sql_execute(sqldb.create_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "Mel", "Move", "melmove@microsoft.com", "melpass", False))
    
    # Create Report
    sqldb.sql_execute(sqldb.create_report("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "9e29f498-2b9f-3c1e-8fd6-fb74a6fd26f8", 50, "This is the report."))
    sqldb.sql_execute(sqldb.create_report("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "9e29f498-2b9f-3c1e-8fd6-fb74a6fd26f8", 50, "I reported something."))
    sqldb.sql_execute(sqldb.create_report("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "9e29f498-2b9f-3c1e-8fd6-fb74a6fd26f8", 50, "Yes and no."))
    sqldb.sql_execute(sqldb.create_report("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "a0d3146f-2673-3860-9c36-1d37f8194dc4", 50, "Another report here."))

    # Print Organizations
    sqldb.print_table("accounts")
    print()
    # Print Users
    sqldb.print_table("users")
    print()
    # Print Reports
    sqldb.print_table("reports")
    print()

    # Remove User without reports
    sqldb.remove_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "microsoft@microsoft.com", "heatherwills@microsoft.com", "securepass", False)

    print("\n\n-----------------------------------------------------------------------------------------------------------------------------\n")
    print("Removed heatherwills@microsoft.com without reports")
    # Print Organizations
    sqldb.print_table("accounts")
    print()
    # Print Users
    sqldb.print_table("users")
    print()
    # Print Reports
    sqldb.print_table("reports")
    print()

    # Remove User with reports
    sqldb.remove_user("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "microsoft@microsoft.com", "georgejace@microsoft.com", "securepass", True)

    print("\n\n-----------------------------------------------------------------------------------------------------------------------------\n")
    print("Removed georgejace@microsoft.com with reports")
    # Print Organizations
    sqldb.print_table("accounts")
    print()
    # Print Users
    sqldb.print_table("users")
    print()
    # Print Reports
    sqldb.print_table("reports")
    print()

    # Remove Report
    sqldb.remove_report("ff7b23e8-0cc5-35fe-a472-8c1c277494ea", "microsoft@microsoft.com", "a608fb04-b110-308b-9d43-92554512cf43", "securepass")
    print("\n\n-----------------------------------------------------------------------------------------------------------------------------\n")
    print("Removed Report - Should show no reports")
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
    print("Removed Microsoft organization")
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