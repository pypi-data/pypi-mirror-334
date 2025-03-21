# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectTaskUpdate(models.Model):
    _name = "project.task.update"

    task_id = fields.Many2one(
        comodel_name="project.task",
        string="Task",
        ondelete="cascade",
    )
    date = fields.Date(
        string="Date", required=True, default=lambda self: fields.Date.today()
    )
    execution_pcnt = fields.Float(
        string="Execution percent", help="Execution percent of the task"
    )
    description = fields.Char(string="Description")
    currency_id = fields.Many2one(
        related="task_id.project_id.analytic_account_id.company_id.currency_id",
        string="Currency",
    )
    name = fields.Char(string="Name", related="task_id.name")
    is_editable = fields.Boolean(compute="_compute_editable", store=False)
    budget_amount = fields.Monetary(
        string="Budget Amount", related="task_id.budget_amount"
    )
    current_execution = fields.Float(
        string="Current execution", compute="_compute_excecution_pcnt", store=True
    )

    @api.depends("execution_pcnt", "budget_amount")
    def _compute_excecution_pcnt(self):
        for record in self:
            record.current_execution = (
                record.execution_pcnt * record.budget_amount / 100
            )

    @api.depends("date")
    def _compute_editable(self):
        for upd in self:
            upd.is_editable = upd.date > (date.today() - relativedelta(months=1))
