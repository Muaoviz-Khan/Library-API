"""create user and book table

Revision ID: 5e3b49260b0d
Revises: dda9d9e7abc6
Create Date: 2024-06-28 16:51:23.713697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e3b49260b0d'
down_revision: Union[str, None] = 'dda9d9e7abc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("user",sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50)),     
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('_password' ,sa.String(700), nullable=False),
        sa.Column('email', sa.String(30), nullable=False, unique=True),
        sa.Column('status', sa.String(10),nullable=True))

    op.create_table("book",sa.Column("id",sa.Integer, primary_key=True),
    sa.Column("title",sa.String(30), nullable=False),
    sa.Column("publication_date",sa.Date, nullable=True),
    sa.Column("genre",sa.String(50)),
    sa.Column("count",sa.Integer,nullable=True),
    sa.Column('author_name', sa.String(30), sa.ForeignKey('author.name'), nullable=True)
    )
    
    op.create_table(
        'user_books',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
        sa.Column('book_id', sa.Integer, sa.ForeignKey('book.id'), primary_key=True)
    )


def downgrade() -> None:
    op.drop_table('user')

    op.drop_table('book')
    op.drop_table('user_book')
