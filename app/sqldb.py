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


def get_account(organization_email, organization_password):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id char(36) NOT NULL UNIQUE,
            name varchar NOT NULL UNIQUE,
            email varchar NOT NULL UNIQUE,
            password varchar NOT NULL
        );
        SELECT * FROM accounts
        WHERE (email = '{0}' AND password = '{1}');
        """.format(organization_email, encrypt_pass(organization_password)))
        return cur.fetchone()


def get_user(user_email: str, organization_email: str=None, user_password: str=None, organization_password: str=None):
    with conn.cursor() as cur:
        if user_password != None:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id char(36) NOT NULL UNIQUE,
                organization_id char(36) NOT NULL,
                firstname varchar NOT NULL,
                lastname varchar NOT NULL,
                email varchar NOT NULL UNIQUE,
                password varchar NOT NULL,
                type boolean NOT NULL
            );
            SELECT * FROM users
            WHERE (email = '{0}' AND password = '{1}');
            """.format(user_email, encrypt_pass(user_password)))
        elif organization_email != None and organization_password != None:
            if get_account(organization_email, organization_password) != None:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id char(36) NOT NULL UNIQUE,
                    organization_id char(36) NOT NULL,
                    firstname varchar NOT NULL,
                    lastname varchar NOT NULL,
                    email varchar NOT NULL UNIQUE,
                    password varchar NOT NULL,
                    type boolean NOT NULL
                );
                SELECT * FROM users
                WHERE (email = '{0}');
                """.format(user_email))
            else:
                return None
        else:
            return None
        return cur.fetchone()


def get_report(organization_id: str, report_id: str):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id char(36) NOT NULL UNIQUE,
            organization_id char(36) NOT NULL,
            user_id char(36) NOT NULL,
            severity smallint NOT NULL,
            report text NOT NULL
        );
        SELECT * FROM reports
        WHERE (organization_id = '{0}' AND id = '{1}');
        """.format(organization_id, report_id))
        return cur.fetchone()


def remove_account(organization_id: str, organization_email: str, organization_password: str): # returns boolean if deletion was successful
    with conn.cursor() as cur:
        if get_account(organization_id, organization_email, organization_password) != None:
            cur.execute("""
            DELETE FROM users
            WHERE organization_id = '{0}';
            DELETE FROM reports
            WHERE organization_id = '{0}';
            DELETE FROM accounts
            WHERE id = '{0}';
            """.format(organization_id))
            return True
        return False


def remove_user(organization_id: str, organization_email: str, user_email: str, organization_password: str, remove_user_reports: bool): # returns boolean if deletion was successful
    with conn.cursor() as cur:
        if get_user(organization_id, user_email, organization_email=organization_email, organization_password=organization_password) != None:
            user_id = get_user(organization_id, user_email, organization_email=organization_email, organization_password=organization_password)[0]
            if remove_user_reports:
                cur.execute("""
                DELETE FROM reports
                WHERE (organization_id = '{0}' AND user_id = '{1}');
                """.format(organization_id, user_id))
            cur.execute("""
            DELETE FROM users
            WHERE (organization_id = '{0}' AND email = '{1}');
            """.format(organization_id, user_email))
            return True
        return False


def remove_report(organization_id: str, organization_email: str, report_id: str, organization_password: str):
    with conn.cursor() as cur:
        if get_account(organization_id, organization_email, organization_password) != None and get_report(organization_id, report_id) != None:
            cur.execute("""
            DELETE FROM reports
            WHERE (organization_id = '{0}' AND id = '{1}')
            """.format(organization_id, report_id))
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