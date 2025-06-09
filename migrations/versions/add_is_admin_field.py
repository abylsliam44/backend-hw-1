"""add is_admin field

Revision ID: add_is_admin_field
Revises: 
Create Date: 2024-03-09 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_is_admin_field'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add is_admin column with default value False
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.execute('UPDATE users SET is_admin = FALSE WHERE is_admin IS NULL')
    op.alter_column('users', 'is_admin', nullable=False, server_default=sa.text('FALSE'))

def downgrade():
    # Remove is_admin column
    op.drop_column('users', 'is_admin') 