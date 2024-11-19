"""update fields

Revision ID: 0e99539a55e0
Revises: 2b2c8c7efe81
Create Date: 2024-11-19 12:38:16.494551

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e99539a55e0"
down_revision: Union[str, None] = "2b2c8c7efe81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
