import sqlalchemy as sa


METADATA = sa.MetaData()

CONTENT_TABLE = sa.Table(
    "content",
    METADATA,
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("url", sa.String(1024), nullable=False, unique=True),
    sa.Column("body", sa.Text, nullable=True),
)

BOT_TABLE = sa.Table(
    "bot",
    METADATA,
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("secret_id", sa.String(255), nullable=False),
    sa.Column("client_id", sa.String(255), nullable=False),
    sa.Column("nickname", sa.String(255), nullable=False),
    sa.Column(
        "load",
        sa.Integer,
        nullable=False,
        default=0,
    ),
    sa.Column(
        "max_load",
        sa.Integer,
        nullable=False,
        default=40,
    ),
)

USER_TABLE = sa.Table(
    "user",
    METADATA,
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("nicknames", sa.ARRAY(sa.String(255)), nullable=False),
    sa.Column("ext_id", sa.Integer, nullable=False),
)

MESSAGE_TABLE = sa.Table(
    "message",
    METADATA,
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("content", sa.String(255), nullable=False),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
    sa.Column(
        "channel_id",
        sa.Integer,
        sa.ForeignKey("channel.id"),
        nullable=False,
    ),
)

CHANNEL_TABLE = sa.Table(
    "channel",
    METADATA,
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("url", sa.String(255), nullable=False),
    sa.Column("start_listen_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("ping_listen_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("stop_listen_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column(
        "listen_bot_id", sa.Integer, sa.ForeignKey("bot.id"), nullable=True
    ),
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
