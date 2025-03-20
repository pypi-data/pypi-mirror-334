# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

import datetime
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    execution_weight = fields.Selection(
        [
            ("budget", "Based on phase budget [new field on task]"),
            ("hours", "Based on calculated hours"),
            ("none", "No autocalculation"),
        ],
        string="How should we weight each task?",
        default="budget",
    )
    total_budget = fields.Monetary("Total Budget", tracking=True)
    hourly_price = fields.Monetary("Hourly Price", tracking=True)
    last_update_percent = fields.Float(related="last_update_id.progress", store=True)
    last_update_execution_pcnt = fields.Float(
        related="last_update_id.progress", store=True
    )
    last_update_execution_amount = fields.Monetary(
        related="last_update_id.total_execution", store=True
    )
    last_update_total_hours = fields.Float(
        related="last_update_id.total_hours", store=True
    )
    last_update_material_expenses = fields.Monetary(
        related="last_update_id.material_expenses", store=True
    )
    last_update_total_incomes = fields.Monetary(
        related="last_update_id.total_incomes", store=True
    )
    allocated_hours = fields.Float(
        string="Allocated Hours", compute="_compute_allocated_hours"
    )
    hourly_expenses = fields.Monetary(compute="_compute_hourly_expenses", store=True)
    total_expenses = fields.Monetary(compute="_compute_total_expenses", store=True)
    balance_hours = fields.Float(compute="_compute_balance_hours", store=True)
    execution_amount = fields.Monetary(string="Execution amount")
    execution_kpi = fields.Monetary(compute="_compute_kpi_execution", store=True)
    real_time_evaluation = fields.Float(
        related="last_update_id.real_time_evaluation", store=True
    )

    @api.depends("hourly_price", "allocated_hours")
    def _compute_hourly_expenses(self):
        for record in self:
            record.hourly_expenses = record.hourly_price * record.allocated_hours

    @api.depends("hourly_expenses", "last_update_id.material_expenses")
    def _compute_total_expenses(self):
        for record in self:
            record.total_expenses = (
                record.hourly_expenses + record.last_update_id.material_expenses
            )

    @api.depends("last_update_id.total_execution", "total_expenses")
    def _compute_balance_hours(self):
        for record in self:
            record.balance_hours = (
                record.last_update_id.total_execution - record.total_expenses
            )

    @api.depends(
        "last_update_id.total_execution",
        "last_update_id.material_expenses",
        "allocated_hours",
    )
    def _compute_kpi_execution(self):
        for record in self:
            record.execution_kpi = (
                record.last_update_id.total_execution
                - record.last_update_id.material_expenses
            ) / record.allocated_hours

    def project_recalculate_execution(self, date):
        for project in self:
            if project.execution_weight == "none":
                next

            executed = 0
            total = 0
            task_updates = []
            for task in project.task_ids:
                _logger.debug(
                    "Last update project weight type -%s- ", project.execution_weight
                )
                if project.execution_weight == "budget":
                    total = total + task.budget_amount
                    _logger.debug("Last update date %s ", date)
                    last_update = self.env["project.task.update"].search(
                        [("task_id", "=", task.id), ("date", "<=", date)],
                        order="date desc",
                        limit=1,
                    )
                    # list_updates= task.task_update_ids.filtered(lambda l: l.date <= date).sorted(lambda m: m.date,reverse=True)
                    if last_update:
                        # last_update = list_updates[0]
                        _logger.debug(
                            "Last update for task executed pcnt %s - %s",
                            last_update.execution_pcnt,
                            date,
                        )
                        executed = executed + (
                            task.budget_amount * last_update.execution_pcnt / 100
                        )
                        task_updates.append(last_update.id)
                    else:
                        task_update = self.env["project.task.update"].create(
                            {
                                "task_id": task.id,
                                "execution_pcnt": 0,
                                "description": f"Automatic",
                                "date": date,
                            }
                        )
                        task_updates.append(task_update.id)

                elif project.execution_weight == "hours":
                    total = total + task.planned_hours
                    executed = executed + task.effective_hours
                    task_updates.append(task.id)

                _logger.debug(
                    "Last update for task executed %s - total %s", executed, total
                )
            if total > 0:
                project_total_pcnt = 100 * executed / total
                project_total_executtion = executed
            else:
                project_total_pcnt = 0
                project_total_executtion = 0
            acls = self.env["account.analytic.line"].search(
                [("account_id", "=", project.analytic_account_id.id)]
            )
            hours = 0
            expenses = 0
            incomes = 0
            real_time_expenses = 0
            for acl in acls:
                if acl.date <= date:
                    if acl.product_uom_id.id == self.env.ref("uom.product_uom_hour").id:
                        hours = hours + acl.unit_amount
                        real_time_expenses = real_time_expenses + acl.amount
                    else:
                        if acl.amount < 0:
                            expenses = expenses - acl.amount
                        else:
                            incomes = incomes + acl.amount

            if project.update_ids or project_total_pcnt > 0:
                existing_update = self.env["project.update"].search(
                    [
                        ("project_id", "=", project.id),
                        ("date", "=", date),
                        ("auto", "=", True),
                    ]
                )
                if existing_update:
                    existing_update.write(
                        {
                            "progress": project_total_pcnt,
                            "progress_percentage": project_total_pcnt,
                            "total_budget": total,
                            "total_execution": project_total_executtion,
                            "total_hours": hours,
                            "material_expenses": expenses,
                            "total_incomes": incomes,
                            "project_task_update_ids": [(6, 0, task_updates)],
                            "real_time_evaluation": real_time_expenses,
                        }
                    )
                else:
                    self.env["project.update"].create(
                        {
                            "status": "on_track",
                            "total_budget": total,
                            "project_id": project.id,
                            "name": f"Automatic update for {date:%d/%m/%Y}",
                            "auto": True,
                            "progress": project_total_pcnt,
                            "progress_percentage": project_total_pcnt,
                            "total_execution": project_total_executtion,
                            "date": date,
                            "total_hours": hours,
                            "material_expenses": expenses,
                            "total_incomes": incomes,
                            "project_task_update_ids": [(6, 0, task_updates)],
                            "real_time_evaluation": real_time_expenses,
                        }
                    )

    @api.model
    def recalc_execution_active_projects(self):
        last_month_date = datetime.date.today().replace(day=1) - datetime.timedelta(
            days=1
        )
        for record in self:
            record.project_recalculate_execution(last_month_date)

    @api.depends("task_ids.planned_hours")
    def _compute_allocated_hours(self):
        for record in self:
            task_ids = self.env["project.task"].search([("project_id", "=", record.id)])
            planned_hours = 0
            for task_id in task_ids:
                planned_hours += task_id.planned_hours
                record.allocated_hours = planned_hours
