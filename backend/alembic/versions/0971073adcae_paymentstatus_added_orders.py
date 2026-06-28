"""PaymentStatus Added Orders"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0971073adcae"
down_revision: Union[str, None] = "53f04bc0f39b"
branch_labels = None
depends_on = None


payment_status_enum = postgresql.ENUM(
    "PENDING",
    "PAID",
    "FAILED",
    "REFUNDED",
    name="paymentstatus",
)


def upgrade():

    payment_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "orders",
        sa.Column(
            "payment_status",
            payment_status_enum,
            nullable=False,
            server_default="PENDING",
        ),
    )


def downgrade():

    op.drop_column("orders", "payment_status")

    payment_status_enum.drop(op.get_bind(), checkfirst=True)
