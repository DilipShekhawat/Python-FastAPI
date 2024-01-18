"""create vote table

Revision ID: 42dafd650c75
Revises: 9aabc4903d55
Create Date: 2024-01-18 13:25:00.573580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42dafd650c75'
down_revision: Union[str, None] = '9aabc4903d55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id',sa.Integer(),sa.ForeignKey("users.id", ondelete="CASCADE"),primary_key=True,nullable=False),
                    sa.Column('post_id',sa.Integer(),sa.ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True,nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass
