"""complete ZH sample data

Revision ID: c9f3b1a8e2d0
Revises: b4e1775f1e7c
Create Date: 2026-02-04 00:00:00.000000

"""

import importlib
from pathlib import Path

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "c9f3b1a8e2d0"
down_revision = "b4e1775f1e7c"
branch_labels = None
depends_on = None


def upgrade():
    _write_sample_picture()
    data = text(
        importlib.resources.read_text("gn_module_zh.migrations.data", "insert_into_complete_zh.sql")
    )
    op.get_bind().execute(data)


def downgrade():
    data = text(
        importlib.resources.read_text("gn_module_zh.migrations.data", "delete_complete_zh.sql")
    )
    op.get_bind().execute(data)


def _write_sample_picture():
    b64_text = importlib.resources.read_text("gn_module_zh.migrations.data", "sample_zh.jpg.b64")
    if "BASE64_PLACEHOLDER" in b64_text or not b64_text.strip():
        return
    b64_text = b64_text.strip()
    if b64_text.startswith("data:"):
        b64_text = b64_text.split(",", 1)[-1]
    b64_text = "".join(b64_text.split())
    try:
        import base64

        image_bytes = base64.b64decode(b64_text)
    except Exception:
        return
    try:
        from geonature.utils.env import BACKEND_DIR
    except Exception:
        backend_dir = Path(__file__).resolve().parents[2]
    else:
        backend_dir = BACKEND_DIR
    attachments_dir = backend_dir / "media" / "attachments"
    attachments_dir.mkdir(parents=True, exist_ok=True)
    image_path = attachments_dir / "sample_zh.jpg"
    if not image_path.exists():
        image_path.write_bytes(image_bytes)
