"""Initial security and anonymous chat history tables.

Revision ID: 20260409_0001
Revises:
Create Date: 2026-04-09 00:00:00
"""

from __future__ import annotations

from alembic import op

revision = "20260409_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR NOT NULL UNIQUE,
            display_name VARCHAR NULL,
            role VARCHAR NOT NULL,
            oidc_subject VARCHAR NULL,
            issuer VARCHAR NULL,
            password_hash VARCHAR NULL,
            is_active BOOLEAN NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_id ON users (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_email ON users (email)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_users_oidc_subject ON users (oidc_subject)"
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id SERIAL PRIMARY KEY,
            anonymous_user_key VARCHAR(64) NOT NULL,
            title VARCHAR(255) NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_chats_id ON chats (id)")
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_chats_anonymous_user_key
        ON chats (anonymous_user_key)
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_chats_updated_at ON chats (updated_at)"
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            chat_id INTEGER NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
            sender_type VARCHAR(32) NOT NULL,
            content_masked TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_messages_id ON messages (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_messages_chat_id ON messages (chat_id)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_messages_created_at ON messages (created_at)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_messages_created_at")
    op.execute("DROP INDEX IF EXISTS ix_messages_chat_id")
    op.execute("DROP INDEX IF EXISTS ix_messages_id")
    op.execute("DROP TABLE IF EXISTS messages")

    op.execute("DROP INDEX IF EXISTS ix_chats_updated_at")
    op.execute("DROP INDEX IF EXISTS ix_chats_anonymous_user_key")
    op.execute("DROP INDEX IF EXISTS ix_chats_id")
    op.execute("DROP TABLE IF EXISTS chats")

    op.execute("DROP INDEX IF EXISTS ix_users_oidc_subject")
    op.execute("DROP INDEX IF EXISTS ix_users_email")
    op.execute("DROP INDEX IF EXISTS ix_users_id")
    op.execute("DROP TABLE IF EXISTS users")
