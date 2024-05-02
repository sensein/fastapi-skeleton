# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# DISCLAIMER: This software is provided "as is" without any warranty,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose, and non-infringement.
#
# In no event shall the authors or copyright holders be liable for any
# claim, damages, or other liability, whether in an action of contract,
# tort, or otherwise, arising from, out of, or in connection with the
# software or the use or other dealings in the software.
# -----------------------------------------------------------------------------
from datetime import datetime

# @Author  : Tek Raj Chhetri
# @Email   : tekraj@mit.edu
# @Web     : https://tekrajchhetri.com/
# @File    : database.py
# @Software: PyCharm
import asyncpg
from fastapi import HTTPException

from core.configuration import load_environment

DB_SETTINGS = {
    "user": load_environment()["JWT_POSTGRES_DATABASE_USER"],
    "password": load_environment()["JWT_POSTGRES_DATABASE_PASSWORD"],
    "database": load_environment()["JWT_POSTGRES_DATABASE_NAME"],
    "host": load_environment()["JWT_POSTGRES_DATABASE_HOST_URL"],
    "port": load_environment()["JWT_POSTGRES_DATABASE_PORT"],
}

table_name_user = load_environment()["JWT_POSTGRES_TABLE_USER"]
table_name_scope = load_environment()["JWT_POSTGRES_TABLE_SCOPE"]
table_relation = load_environment()["JWT_POSTGRES_TABLE_USER_SCOPE_REL"]


async def connect_postgres():
    try:
        connection = await asyncpg.connect(**DB_SETTINGS)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def close_db_connection(conn):
    await conn.close()


async def insert_data(conn, fullname, email, password):
    try:

        pg_query = f"""
            INSERT INTO \"{table_name_user}\" (full_name, email, password, is_active, created_at, updated_at) 
            VALUES ($1, $2, $3, $4, $5, $6) RETURNING id
        """
        jwt_user_id = await conn.fetchval(
            pg_query,
            fullname,
            email,
            password,
            False,
            datetime.utcnow(),
            datetime.utcnow(),
        )

        scope_exist_id = await select_scope_id(conn)
        if not scope_exist_id:
            # First insert the default read access
            scope_query_exist_case = f"""
            INSERT INTO \"{table_name_scope}\" (name, description, created_at, updated_at) 
            VALUES ($1, $2, $3, $4,) RETURNING id"""

            new_scope_id = await conn.fetchval(
                scope_query_exist_case,
                "read",
                "This allows read access",
                datetime.utcnow(),
                datetime.utcnow(),
            )

            # now connect with rel
            await conn.execute(
                f"""INSERT INTO \"{table_relation}\" (jwtuser_id, scope_id) VALUES ($1, $2)""",
                jwt_user_id,
                new_scope_id,
            )
        else:
            await conn.execute(
                f"""INSERT INTO \"{table_relation}\" (jwtuser_id, scope_id) VALUES ($1, $2)""",
                jwt_user_id,
                scope_exist_id,
            )

        return {
            "detail": "Registration completed successfully! Admin will activate your account after verification."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def insert_scope(conn):
    try:
        row = await conn.fetchrow(
            "SELECT id FROM \"{table_name_scope}\" WHERE NAME = 'read'"
        )
        if row:
            return row
        return False
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def select_scope_id(conn):
    try:
        scope_id = await conn.fetchval(
            "SELECT id FROM \"{table_name_scope}\" WHERE NAME = 'read' LIMIT 1"
        )
        return scope_id  # Returns the user ID if found, or None if no user exists
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_scopes_by_user(user_id):
    conn = await connect_postgres()
    query = f"""SELECT s.name
    FROM \"{table_name_scope}\" s
    JOIN \"{table_relation}\" js ON s.id = js.scope_id
    WHERE js.jwtuser_id =  $1"""
    try:
        results = await conn.fetch(query, user_id)
        assigned_scopes_to_user = [result["name"] for result in results]
        print("*" * 100)
        print(assigned_scopes_to_user)
        print("#" * 100)
        return assigned_scopes_to_user
    finally:
        # Ensure the connection is closed even if an error occurs
        await conn.close()


async def get_user(conn=None, email=None):
    try:
        if conn is None:
            conn = await connect_postgres()
        query = """
        SELECT * FROM "{}" WHERE email = $1 LIMIT 1
        """.format(
            table_name_user
        )
        row = await conn.fetchrow(query, email)
        if row:
            return row
        return False
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
