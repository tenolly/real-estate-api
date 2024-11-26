"""source.last_check_ts datetime -> bigint

Revision ID: 704d694c93f8
Revises: 0e99539a55e0
Create Date: 2024-11-27 01:23:35.991717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "704d694c93f8"
down_revision: Union[str, None] = "0e99539a55e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
