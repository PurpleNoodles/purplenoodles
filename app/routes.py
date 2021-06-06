from flask.templating import render_template
from app import app, config, sqldb, nlp
from flask import render_template, redirect, url_for, request, session

app.secret_key = config['SECRET_KEY']

report_text = """
I am writing to inform you that my immediate supervisor, Joseph Adams, has been sexually harassing me while I am trying to perform my work duties here at Johnson Publishing. The harassment started about two months ago. Mr. Adams came up behind me at my desk, started rubbing my shoulders, and told me that if I would start spending more time with him then I could advance into another position quickly. I told him I wasn’t interested, and he responded, “not yet.” Another employee, Sarah Atkins, was seated two desks away and looked toward me and shook her head, so I am sure she overheard the conversation. 

About a month ago, Mr. Adams approached me near the copy machine and asked me if I had changed my mind. I asked what he was referring to, and he said, “Do you still want that promotion? If you do, then you can earn some bonus points by spending some time with me after work.” I once again responded that I wasn’t interested and told him he was making me feel uncomfortable. 

Two days ago, on Wednesday of this week, Mr. Adams told me that if I couldn’t agree to spend more time with him after work, I will not move up in the company. He also said that I will most likely be transferred into another department. Rebekah Jefferson overhead the discussion and later told me that Mr. Adams always gets his way so I should probably reconsider. 

This kind of behavior is unacceptable, and I am sure that Johnson Publishing does not condone this activity. I ask you to properly investigate this matter and put an end to this inappropriate treatment.
"""


# Drop tables
sqldb.sql_execute(sqldb.drop_tables())

@app.route('/')
def landing():
    if 'user_id' in session:
        print(session['user_id'])
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect('/home')
    if request.method == 'POST':
        sqldb.sql_execute(sqldb.create_account(
            request.form['orgName'],
            request.form['orgEmail'],
            request.form['password']
        ))
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/home')
    if request.method == 'POST':
        db_user = sqldb.get_user(
            request.form['email'],
            user_password=request.form['password']
        )
        if db_user != None:
            session['user_id'] = db_user[0]
            session['organization_id'] = db_user[1]
            session['firstname'] = db_user[2]
            session['lastname'] = db_user[3]
            session['email'] = db_user[4]
            session['type'] = db_user[6]
        return redirect('/home')
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    
    if 'user_id' not in session:
        return redirect('/')
    else:
        if session['type']:
            return render_template('users.html')
        else:
            return render_template('user_text.html')

@app.route('/users')
@app.route('/user_text')
def user_redirect():
    if 'user_id' not in session:
        return redirect('/')
    else:
        return redirect('/home')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'user_id' not in session:
        return redirect('/')
    else:
        if session['type']:
            sqldb.sql_execute(sqldb.create_report('ff7b23e8-0cc5-35fe-a472-8c1c277494ea', '9e29f498-2b9f-3c1e-8fd6-fb74a6fd26f8', -3, test_reporting()))
            # sqldb.print_table("reports")
            return render_template('report.html')
        else:
            return redirect('/home')

@app.route('/report/<report_id>')
def open_report(report_id: str):
    if 'user_id' not in session:
        return redirect('/')
    else:
        if session['type']:
            found_report = sqldb.get_report(session['organization_id'], str(report_id))
            if found_report != None:
                return str(found_report[4])
            else:
                return "Could not find report or you do not have access to this report."
        else:
            return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('organization_id', None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    session.pop('email', None)
    session.pop('type', None)
    return redirect('/')

def test_reporting():
    the_report = nlp.generate_report(report_text, {
        'user_id': '9e29f498-2b9f-3c1e-8fd6-fb74a6fd26f8',
        'organization_id': 'ff7b23e8-0cc5-35fe-a472-8c1c277494ea',
        'firstname': 'John',
        'lastname': 'Smith',
        'email': 'johnsmith@microsoft.com'
    })
    return str(the_report['report'])

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