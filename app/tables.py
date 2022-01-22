import sqlalchemy as sa

from .providers import METADATA


CHANNEL_TABLE = sa.Table(
    "channel",
    METADATA,
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("url", sa.String(255), nullable=False),
    sa.Column("start_listen_at", sa.Boolean, nullable=True),
    sa.Column("ping_listen_at", sa.Boolean, nullable=True),
    sa.Column("stop_listen_at", sa.Boolean, nullable=True),
    sa.Column(
        "ignore",
        sa.Boolean,
        nullable=False,
        default=False,
    ),
    sa.Column(
        "active",
        sa.Boolean,
        nullable=False,
        default=False,
    ),
)
