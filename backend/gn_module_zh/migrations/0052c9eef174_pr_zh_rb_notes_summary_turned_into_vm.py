"""pr_zh.rb_notes_summary turned into vm

Revision ID: 0052c9eef174
Revises: da5b95b24f06
Create Date: 2024-12-16 12:27:35.433511

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0052c9eef174"
down_revision = "da5b95b24f06"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            DROP VIEW pr_zh.rb_notes_summary;

            -- pr_zh.rb_notes_summary source
            CREATE materialized VIEW pr_zh.rb_notes_summary AS
            SELECT
                rb.name AS bassin_versant,
                COALESCE(rub1.note, 0) + COALESCE(rub2.note, 0) + COALESCE(rub3.note, 0) + COALESCE(rub4.note, 0) + COALESCE(rub5.note, 0) + COALESCE(rub6.note, 0) + COALESCE(rub7.note, 0) + COALESCE(rub8.note, 0) AS global_note,
                COALESCE(rub1.note, 0) + COALESCE(rub2.note, 0) + COALESCE(rub3.note, 0) + COALESCE(rub4.note, 0) + COALESCE(rub5.note, 0) AS volet_1,
                COALESCE(rub6.note, 0) + COALESCE(rub7.note, 0) + COALESCE(rub8.note, 0) AS volet_2,
                rub1.note AS rub_sdage,
                rub2.note AS rub_interet_pat,
                rub3.note AS rub_eco,
                rub4.note AS rub_hydro,
                rub5.note AS rub_socio,
                rub6.note AS rub_statut,
                rub7.note AS rub_etat_fonct,
                rub8.note AS rub_menaces
            FROM
                pr_zh.t_river_basin rb
                RIGHT JOIN pr_zh.cor_rb_rules rb_rules ON rb.id_rb = rb_rules.rb_id
                JOIN (
                    SELECT
                        get_cat_note_without_subcats.rb_id,
                        get_cat_note_without_subcats.note
                    FROM
                        pr_zh.get_cat_note_without_subcats(1) get_cat_note_without_subcats(rb_id, note)
                ) rub1 ON rub1.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(2) get_cat_note_with_subcats(rb_id, note)
                ) rub2 ON rub2.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_without_subcats.rb_id,
                        get_cat_note_without_subcats.note
                    FROM
                        pr_zh.get_cat_note_without_subcats(3) get_cat_note_without_subcats(rb_id, note)
                ) rub3 ON rub3.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(4) get_cat_note_with_subcats(rb_id, note)
                ) rub4 ON rub4.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(5) get_cat_note_with_subcats(rb_id, note)
                ) rub5 ON rub5.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(6) get_cat_note_with_subcats(rb_id, note)
                ) rub6 ON rub6.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(7) get_cat_note_with_subcats(rb_id, note)
                ) rub7 ON rub7.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_without_subcats.rb_id,
                        get_cat_note_without_subcats.note
                    FROM
                        pr_zh.get_cat_note_without_subcats(8) get_cat_note_without_subcats(rb_id, note)
                ) rub8 ON rub8.rb_id = rb.id_rb
            GROUP BY
                rb.id_rb,
                rb.name,
                rub1.note,
                rub2.note,
                rub3.note,
                rub4.note,
                rub5.note,
                rub6.note,
                rub7.note,
                rub8.note
            ORDER BY
                rb.id_rb;
        """
    )


def downgrade():
    op.execute(
        """
            DROP MATERIALIZED VIEW pr_zh.rb_notes_summary;

            -- pr_zh.rb_notes_summary source
            CREATE VIEW pr_zh.rb_notes_summary AS
            SELECT
                rb.name AS bassin_versant,
                COALESCE(rub1.note, 0) + COALESCE(rub2.note, 0) + COALESCE(rub3.note, 0) + COALESCE(rub4.note, 0) + COALESCE(rub5.note, 0) + COALESCE(rub6.note, 0) + COALESCE(rub7.note, 0) + COALESCE(rub8.note, 0) AS global_note,
                COALESCE(rub1.note, 0) + COALESCE(rub2.note, 0) + COALESCE(rub3.note, 0) + COALESCE(rub4.note, 0) + COALESCE(rub5.note, 0) AS volet_1,
                COALESCE(rub6.note, 0) + COALESCE(rub7.note, 0) + COALESCE(rub8.note, 0) AS volet_2,
                rub1.note AS rub_sdage,
                rub2.note AS rub_interet_pat,
                rub3.note AS rub_eco,
                rub4.note AS rub_hydro,
                rub5.note AS rub_socio,
                rub6.note AS rub_statut,
                rub7.note AS rub_etat_fonct,
                rub8.note AS rub_menaces
            FROM
                pr_zh.t_river_basin rb
                RIGHT JOIN pr_zh.cor_rb_rules rb_rules ON rb.id_rb = rb_rules.rb_id
                JOIN (
                    SELECT
                        get_cat_note_without_subcats.rb_id,
                        get_cat_note_without_subcats.note
                    FROM
                        pr_zh.get_cat_note_without_subcats(1) get_cat_note_without_subcats(rb_id, note)
                ) rub1 ON rub1.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(2) get_cat_note_with_subcats(rb_id, note)
                ) rub2 ON rub2.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_without_subcats.rb_id,
                        get_cat_note_without_subcats.note
                    FROM
                        pr_zh.get_cat_note_without_subcats(3) get_cat_note_without_subcats(rb_id, note)
                ) rub3 ON rub3.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(4) get_cat_note_with_subcats(rb_id, note)
                ) rub4 ON rub4.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(5) get_cat_note_with_subcats(rb_id, note)
                ) rub5 ON rub5.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(6) get_cat_note_with_subcats(rb_id, note)
                ) rub6 ON rub6.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_with_subcats.rb_id,
                        get_cat_note_with_subcats.note
                    FROM
                        pr_zh.get_cat_note_with_subcats(7) get_cat_note_with_subcats(rb_id, note)
                ) rub7 ON rub7.rb_id = rb.id_rb
                JOIN (
                    SELECT
                        get_cat_note_without_subcats.rb_id,
                        get_cat_note_without_subcats.note
                    FROM
                        pr_zh.get_cat_note_without_subcats(8) get_cat_note_without_subcats(rb_id, note)
                ) rub8 ON rub8.rb_id = rb.id_rb
            GROUP BY
                rb.id_rb,
                rb.name,
                rub1.note,
                rub2.note,
                rub3.note,
                rub4.note,
                rub5.note,
                rub6.note,
                rub7.note,
                rub8.note
            ORDER BY
                rb.id_rb;
        """
    )
