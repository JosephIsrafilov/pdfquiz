import json

from app.database import db_execute, get_db_connection


def fetch_documents():
    with get_db_connection() as connection:
        return db_execute(connection, """
            SELECT d.id, d.title, d.questions_json, d.uploaded_by, d.created_at,
                   u.username AS uploader_name
            FROM documents d
            LEFT JOIN users u ON d.uploaded_by = u.id
            ORDER BY d.id DESC
        """).fetchall()


def fetch_document(document_id: int):
    with get_db_connection() as connection:
        return db_execute(
            connection,
            """
            SELECT d.id, d.title, d.questions_json, d.uploaded_by, d.created_at,
                   u.username AS uploader_name
            FROM documents d
            LEFT JOIN users u ON d.uploaded_by = u.id
            WHERE d.id = %s
            """,
            (document_id,),
        ).fetchone()


def serialize_document(document):
    if document is None:
        return None
    questions = json.loads(document["questions_json"])
    return {
        "id": document["id"],
        "title": document["title"],
        "question_count": len(questions),
        "uploader_name": document["uploader_name"],
        "created_at": str(document["created_at"]),
    }


def save_document(title: str, questions_json: str, uploaded_by: int):
    with get_db_connection() as connection:
        db_execute(
            connection,
            "INSERT INTO documents (title, questions_json, uploaded_by) VALUES (%s, %s, %s)",
            (title, questions_json, uploaded_by),
        )
        connection.commit()


def delete_document(document_id: int):
    with get_db_connection() as connection:
        db_execute(connection, "DELETE FROM documents WHERE id = %s", (document_id,))
        connection.commit()
