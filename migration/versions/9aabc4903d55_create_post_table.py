"""create post table

Revision ID: 9aabc4903d55
Revises: 734433945bc1
Create Date: 2024-01-18 13:21:22.076453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aabc4903d55'
down_revision: Union[str, None] = '734433945bc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id',sa.Integer(), primary_key=True,nullable=False),
                    sa.Column('title',sa.String(), nullable=False),
                    sa.Column('content',sa.String(), nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()')),
                    sa.Column('user_id',sa.Integer(),sa.ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
