"""Add photo field to BannedUser

Revision ID: e7f0b30ef8e8
Revises: 277cc59175ed
Create Date: 2019-08-27 00:42:28.802197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f0b30ef8e8'
down_revision = '277cc59175ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('banned_user', sa.Column('photo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('banned_user', 'photo')
    # ### end Alembic commands ###
