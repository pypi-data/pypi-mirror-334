# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Task(models.Model):
    _inherit = "project.task"

    task_update_ids = fields.One2many(
        string="Task updates",
        comodel_name="project.task.update",
        inverse_name="task_id",
    )
    budget_amount = fields.Monetary(
        string="Budget Amount",
        currency_field="currency_id",
        help="Amount asigned to this task",
    )
    subtasks_budget_amount = fields.Monetary(
        "Subtasks Budget Amount",
        compute="_compute_subtask_effective_hours",
        recursive=True,
        store=True,
        help="Amount asigned on subtasks",
        currency_field="currency_id",
    )
    execution_pcnt = fields.Float(
        string="Execution percent",
        help="Execution percent of the task",
        compute="_compute_last_update",
        store=True,
    )
    currency_id = fields.Many2one(
        related="project_id.analytic_account_id.company_id.currency_id",
        string="Currency",
    )
    project_execution_weight = fields.Selection(
        related="project_id.execution_weight", store=1
    )
    last_task_update = fields.Char(compute="_compute_last_update", store=True)
    execution_value = fields.Float(
        string="Execution value", compute="_compute_execution_value", store=True
    )

    @api.depends("execution_pcnt", "budget_amount")
    def _compute_execution_value(self):
        for record in self:
            record.execution_value = record.execution_pcnt * record.budget_amount

    @api.depends("task_update_ids.date", "task_update_ids.execution_pcnt")
    def _compute_last_update(self):
        selected = False
        for rec in self:
            date_compare = rec.project_id.last_update_id.date
            for tu in rec.task_update_ids:
                if date_compare and tu.date:
                    if tu.date < date_compare:
                        if selected:
                            if tu.date > selected.date:
                                selected = tu
                        else:
                            selected = tu
            if selected and selected.date and selected.execution_pcnt:
                rec.execution_pcnt = selected.execution_pcnt
                rec.last_task_update = selected
            else:
                rec.execution_pcnt = 0

    @api.depends("child_ids.budget_amount", "child_ids.subtasks_budget_amount")
    def _compute_subtask_effective_hours(self):
        for task in self.with_context(active_test=False):
            task.subtasks_budget_amount = sum(
                child_task.budget_amount + child_task.subtasks_budget_amount
                for child_task in task.child_ids
            )
