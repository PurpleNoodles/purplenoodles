import psycopg2
import uuid

conn = psycopg2.connect('')

def sql_execute(sql_command: str):
    with conn.cursor() as cur:
        cur.execute(sql_command)

def create_account(name: str, email: str, password: str):
    id = uuid.uuid3(uuid.NAMESPACE_X500, name)
    return """
    CREATE TABLE IF NOT EXISTS accounts (
        id char(36) NOT NULL UNIQUE,
        name varchar NOT NULL UNIQUE,
        email varchar NOT NULL UNIQUE,
        password text NOT NULL
    );
    INSERT INTO accounts (id, name, email, password)
    VALUES ('{0}', '{1}', '{2}', '{3}')
    ON CONFLICT DO NOTHING;
    """.format(id, name, email, password)

def create_user(organization_id: str, firstname: str, lastname: str, email: str, password: str, type: bool):
    id = uuid.uuid3(uuid.NAMESPACE_URL, organization_id + email)
    return """
    CREATE TABLE IF NOT EXISTS users (
        id char(36) NOT NULL UNIQUE,
        organization_id char(36) NOT NULL,
        firstname varchar NOT NULL,
        lastname varchar NOT NULL,
        email varchar NOT NULL,
        password text NOT NULL,
        type boolean NOT NULL
    );
    INSERT INTO users (id, organization_id, firstname, lastname, email, password, type)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6})
    ON CONFLICT DO NOTHING;
    """.format(id, organization_id, firstname, lastname, email, password, str(type).lower())

def create_report(organization_id: str, user_id: str, severity: int, report: str):
    id = uuid.uuid3(uuid.NAMESPACE_X500, organization_id + user_id + report)
    return """"
    CREATE TABLE IF NOT EXISTS reports (
        id char(36) NOT NULL UNIQUE,
        organization_id char(36) NOT NULL,
        user_id char(36) NOT NULL,
        severity smallint NOT NULL,
        report text NOT NULL
    );
    INSERT INTO reports (id, organization_id, user_id, severity, report)
    VALUES ('{0}', '{1}', '{2}', {3}, '{4}')
    ON CONFLICT DO NOTHING;
    """.format(id, organization_id, user_id, severity, report)

def print_table(table_name: str):
    print("---------- {0} ----------".format(table_name))
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM {0};
        """.format(table_name))
        for row in cur.fetchall():
            print(row)

def drop_tables():
    return """
    DROP TABLE IF EXISTS accounts;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS reports;
    """