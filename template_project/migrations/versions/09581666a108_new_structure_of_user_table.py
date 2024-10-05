"""new structure of User table

Revision ID: 09581666a108
Revises: fa968ceac855
Create Date: 2024-10-04 14:10:46.402314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '09581666a108'
down_revision: Union[str, None] = 'fa968ceac855'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(), nullable=False))
    op.add_column('user', sa.Column('registered_at', sa.TIMESTAMP(), nullable=True))
    op.add_column('user', sa.Column('hashed_password', sa.String(), nullable=False))
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('is_superuser', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.drop_column('user', 'register_data')
    op.drop_column('user', 'fullname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('fullname', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('register_data', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('user', 'is_verified')
    op.drop_column('user', 'is_superuser')
    op.drop_column('user', 'is_active')
    op.drop_column('user', 'hashed_password')
    op.drop_column('user', 'registered_at')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
