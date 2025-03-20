# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class KpiTemplate(models.Model):
    _name = "kpi_template"
    _inherit = ["mixin.master_data"]
    _description = "KPI Template"

    code = fields.Char(
        default="/",
    )
    type = fields.Selection(
        string="Type",
        selection=[
            ("employee", "Employee"),
            ("department", "Department"),
            ("both", "Both"),
        ],
        default="employee",
        required=True,
    )
    kpi_score_categ_id = fields.Many2one(
        string="Score Category",
        comodel_name="kpi_score_categ",
    )
    line_ids = fields.One2many(
        string="Kpi(s)",
        comodel_name="kpi_template_line",
        inverse_name="template_id",
    )
    appraisal_selection_method = fields.Selection(
        string="Appraisal Method",
        selection=[
            ("use_user", "Users"),
            ("use_group", "Groups"),
            ("use_both", "Both specific user and group."),
            ("use_python", "Python Code"),
        ],
        default="use_user",
        required=True,
    )
    user_ids = fields.Many2many(
        string="Users",
        comodel_name="res.users",
        relation="rel_kpi_template_2_users",
        column1="kpi_template_id",
        column2="user_id",
    )
    group_ids = fields.Many2many(
        string="Groups",
        comodel_name="res.groups",
        relation="rel_kpi_template_2_groups",
        column1="kpi_template_id",
        column2="group_id",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void.
#  - user: Return result, the value is list of user.
user = []""",
        copy=True,
    )
    amount_weight = fields.Float(
        string="Total Weight(%)",
        store=True,
        readonly=True,
        compute="_compute_amount_weight",
    )

    @api.depends(
        "line_ids",
        "line_ids.weight",
    )
    def _compute_amount_weight(self):
        for record in self:
            total_weight = 0.0
            for line in record.line_ids:
                total_weight += line.weight
            record.amount_weight = total_weight

    @api.constrains(
        "amount_weight",
    )
    def _check_amount_weight(self):
        for record in self:
            strWarning = _("Total weight cannot be greater than 100.0%")
            if record.amount_weight > 100.0:
                raise UserError(strWarning)
