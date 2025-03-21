# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectUpdate(models.Model):
    _inherit = "project.update"

    auto = fields.Boolean("Is automatic", default=False)
    total_budget = fields.Float("Total Budget", readonly=True)
    execution_pcnt = fields.Float(
        string="Execution percent",
        help="Execution percent of project",
    )
    project_task_update_ids = fields.Many2many(
        "project.task.update", string="Task Updates", help="Task updates"
    )
    currency_id = fields.Many2one(
        related="project_id.analytic_account_id.company_id.currency_id",
        string="Currency",
    )
    project_execution_weight = fields.Selection(
        related="project_id.execution_weight", store=1
    )
    ## Update existing field
    progress = fields.Float(readonly=True)
    total_execution = fields.Monetary("Execution Amount", readonly=True)
    total_hours = fields.Float("Total hours", readonly=True)
    material_expenses = fields.Monetary("Expenses Amount", readonly=True)
    total_incomes = fields.Monetary("Incomes Amount", readonly=True)
    execution_value = fields.Float(
        string="Execution value", compute="_compute_execution_value", store=True
    )
    real_time_evaluation = fields.Float(string="Real time evaluation", readonly=True)

    @api.depends("project_task_update_ids.current_execution")
    def _compute_execution_value(self):
        for record in self:
            record.execution_value = 0
            for task in record.project_task_update_ids:
                record.execution_value += task.current_execution

    def button_recalculate(self):
        self.project_id.project_recalculate_execution(self.date)
