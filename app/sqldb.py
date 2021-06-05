import psycopg2
import uuid
import hashlib

conn = psycopg2.connect('')

def sql_execute(sql_command: str):
    with conn.cursor() as cur:
        cur.execute(sql_command)


def create_account(name: str, email: str, password: str):
    id = uuid.uuid3(uuid.NAMESPACE_URL, name)
    return """
    CREATE TABLE IF NOT EXISTS accounts (
        id char(36) NOT NULL UNIQUE,
        name varchar NOT NULL UNIQUE,
        email varchar NOT NULL UNIQUE,
        password varchar NOT NULL
    );
    INSERT INTO accounts (id, name, email, password)
    VALUES ('{0}', '{1}', '{2}', '{3}')
    ON CONFLICT DO NOTHING;
    """.format(id, name, email, encrypt_pass(password)) + create_user(str(id), "admin", "admin", email, password, True)


def create_user(organization_id: str, firstname: str, lastname: str, email: str, password: str, type: bool):
    id = uuid.uuid3(uuid.NAMESPACE_URL, organization_id + email)
    return """
    CREATE TABLE IF NOT EXISTS users (
        id char(36) NOT NULL UNIQUE,
        organization_id char(36) NOT NULL,
        firstname varchar NOT NULL,
        lastname varchar NOT NULL,
        email varchar NOT NULL UNIQUE,
        password varchar NOT NULL,
        type boolean NOT NULL
    );
    INSERT INTO users (id, organization_id, firstname, lastname, email, password, type)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6})
    ON CONFLICT DO NOTHING;
    """.format(id, organization_id, firstname, lastname, email, encrypt_pass(password), str(type).lower())


def create_report(organization_id: str, user_id: str, severity: int, report: str):
    id = uuid.uuid3(uuid.NAMESPACE_URL, organization_id + user_id + report)
    return """
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


def get_user(user_email, user_password):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM users
        WHERE (email = '{0}' AND password = '{1}')
        """.format(user_email, encrypt_pass(user_password)))
        return cur.fetchone()


def remove_user(organization_id, organization_email, user_email, organization_password): # returns boolean if deletion was successful
    with conn.cursor() as cur:
        if get_user(organization_id, organization_email, organization_password) != None:
            cur.execute("""
            DELETE FROM users
            WHERE (organization_id = '{0}' AND email = '{1}')
            """.format(organization_id, user_email))
            return True
        return False


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

def encrypt_pass(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

# def check_pass(saved_password: str, password: str):
#     return saved_password == hashlib.sha256(password.encode()).hexdigest()