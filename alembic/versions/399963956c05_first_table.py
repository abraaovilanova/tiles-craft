"""first table

Revision ID: 399963956c05
Revises: 
Create Date: 2025-06-23 10:58:36.121274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry 


# revision identifiers, used by Alembic.
revision: str = '399963956c05'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tile",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("src", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("geom", Geometry(geometry_type="POLYGON", srid=4326), nullable=True),  # ✅ Nova coluna

    )


def downgrade() -> None:
    op.drop_table("tile")
