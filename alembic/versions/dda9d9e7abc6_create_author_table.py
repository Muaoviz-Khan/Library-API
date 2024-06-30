"""create author table

Revision ID: dda9d9e7abc6
Revises: 
Create Date: 2024-06-28 16:49:20.194384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dda9d9e7abc6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table("author",sa.Column("name",sa.String(30),primary_key=True)
    ,sa.Column("bio",sa.Text),
    sa.Column("dob",sa.Date, nullable=True))


    

def downgrade() -> None:
    op.drop_table("author")
