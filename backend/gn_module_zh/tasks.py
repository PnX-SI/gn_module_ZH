import os

from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import func
from celery.utils.log import get_task_logger
from celery.schedules import crontab

from flask import current_app
from geonature.utils.celery import celery_app

from geonature.utils.env import db
from geonature.utils.config import config

logger = get_task_logger(__name__)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    ct = config["ZONES_HUMIDES"]["TAXON_VM_CRONTAB"]
    minute, hour, day_of_month, month_of_year, day_of_week = ct.split(" ")
    sender.add_periodic_task(
        crontab(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
        ),
        refresh_taxon_vm.s(),
        name="Refresh taxon vms",
    )


@celery_app.task(bind=True)
def refresh_taxon_vm(self):
    logger.info("Refresh taxon vms...")
    db.session.execute(func.pr_zh.refresh_taxon_materialized_views())
    db.session.commit()
    logger.info("Taxon vms refreshed.")

