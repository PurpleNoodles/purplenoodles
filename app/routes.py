from flask.templating import render_template
from app import app, config
from flask import render_template, redirect, url_for, request
from app.sqldb import sql_execute, create_account, create_user, create_report, print_table, drop_tables

@app.route('/')
def home():
    sql_execute(create_account("Microsoft", "microsoft@microsoft.com", "mysecretpass"))
    print_table("accounts")
    sql_execute(drop_tables())
    return config

