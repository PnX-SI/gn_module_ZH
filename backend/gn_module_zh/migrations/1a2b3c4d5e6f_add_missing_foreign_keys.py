"""Add missing foreign keys

Revision ID: 1a2b3c4d5e6f
Revises: 6f343b68d85f
Create Date: 2026-02-09 16:30:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "1a2b3c4d5e6f"
down_revision = "6f343b68d85f"
branch_labels = None
depends_on = None


def upgrade():

    # #########################################################################
    # Helper to check if constraint exists
    # #########################################################################

    conn = op.get_bind()
    inspector = inspect(conn)

    def constraint_exists(table, constraint_name, schema=None):
        fks = inspector.get_foreign_keys(table, schema=schema)
        for fk in fks:
            if fk["name"] == constraint_name:
                return True
        return False

    def create_fk_with_message_if_missing(
        name,
        table,
        referent_table,
        local_cols,
        remote_cols,
        source_schema,
        referent_schema,
        **kwargs,
    ):
        if constraint_exists(table, name, schema=source_schema):
            return
        try:
            op.create_foreign_key(
                name,
                table,
                referent_table,
                local_cols,
                remote_cols,
                source_schema=source_schema,
                referent_schema=referent_schema,
                **kwargs,
            )
        except (sa.exc.IntegrityError, sa.exc.ProgrammingError, Exception):
            local_col = local_cols[0] if local_cols else "?"
            remote_col = remote_cols[0] if remote_cols else "?"
            print(
                "Impossible de créer la contrainte de clé étrangère "
                f"'{name}' sur la table '{source_schema}.{table}'."
            )
            print(
                "Cela peut être dû à des valeurs orphelines dans le champ "
                f"'{source_schema}.{table}.{local_col}' (qui ne correspondent pas "
                f"à '{referent_schema}.{referent_table}.{remote_col}')."
            )
            raise

    # #########################################################################
    # Add FK - TZH.main_id_rb -> TRiverBasin.id_rb
    # #########################################################################

    create_fk_with_message_if_missing(
        "fk_t_zh_main_id_rb",
        "t_zh",
        "t_river_basin",
        ["main_id_rb"],
        ["id_rb"],
        source_schema="pr_zh",
        referent_schema="pr_zh",
    )

    # #########################################################################
    # Add FK - CorZhArea.id_zh -> TZH.id_zh
    # #########################################################################

    create_fk_with_message_if_missing(
        "fk_cor_zh_area_t_zh",
        "cor_zh_area",
        "t_zh",
        ["id_zh"],
        ["id_zh"],
        source_schema="pr_zh",
        referent_schema="pr_zh",
    )

    # #########################################################################
    # Add FK - TUrbanPlanningDocs.id_area -> LAreas.id_area
    # #########################################################################

    create_fk_with_message_if_missing(
        "fk_t_urban_planning_docs_id_area",
        "t_urban_planning_docs",
        "l_areas",
        ["id_area"],
        ["id_area"],
        source_schema="pr_zh",
        referent_schema="ref_geo",
    )

    # #########################################################################
    # Add FK - CorRbRules.rb_id -> TRiverBasin.id_rb
    # #########################################################################

    create_fk_with_message_if_missing(
        "fk_cor_rb_rules_rb_id",
        "cor_rb_rules",
        "t_river_basin",
        ["rb_id"],
        ["id_rb"],
        source_schema="pr_zh",
        referent_schema="pr_zh",
    )

    # #########################################################################
    # Add FK - CorZhNotes.note_type_id -> BibNoteTypes.note_id
    # #########################################################################

    create_fk_with_message_if_missing(
        "fk_cor_zh_notes_note_type_id",
        "cor_zh_notes",
        "bib_note_types",
        ["note_type_id"],
        ["note_id"],
        source_schema="pr_zh",
        referent_schema="pr_zh",
        onupdate="CASCADE",
    )

    # #########################################################################
    # Add FK - TZH.main_pict_id -> TMedias.id_media
    # #########################################################################

    create_fk_with_message_if_missing(
        "fk_t_zh_main_pict_id",
        "t_zh",
        "t_medias",
        ["main_pict_id"],
        ["id_media"],
        source_schema="pr_zh",
        referent_schema="gn_commons",
        ondelete="SET NULL",
        onupdate="CASCADE",
    )


def downgrade():
    op.drop_constraint("fk_t_zh_main_id_rb", "t_zh", schema="pr_zh", type_="foreignkey")
    op.drop_constraint("fk_cor_zh_area_t_zh", "cor_zh_area", schema="pr_zh", type_="foreignkey")
    op.drop_constraint(
        "fk_t_urban_planning_docs_id_area",
        "t_urban_planning_docs",
        schema="pr_zh",
        type_="foreignkey",
    )
    op.drop_constraint("fk_cor_rb_rules_rb_id", "cor_rb_rules", schema="pr_zh", type_="foreignkey")
    op.drop_constraint(
        "fk_cor_zh_notes_note_type_id", "cor_zh_notes", schema="pr_zh", type_="foreignkey"
    )
    op.drop_constraint("fk_t_zh_main_pict_id", "t_zh", schema="pr_zh", type_="foreignkey")
