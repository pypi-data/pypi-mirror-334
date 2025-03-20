# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiTemplateLine(models.Model):
    _name = "kpi_template_line"
    _description = "KPI Template Line"

    template_id = fields.Many2one(string="#Template", comodel_name="kpi_template")
    kpi_item_id = fields.Many2one(
        string="Item",
        comodel_name="kpi_item",
        required=True,
    )
    weight = fields.Float(
        string="Weight(%)",
        required=True,
    )
    target = fields.Float(
        string="Target",
        required=True,
    )
    realization_method = fields.Selection(
        string="Realization Methods",
        selection=[
            ("user", "User Appraisal"),
            ("python", "Python Code"),
        ],
        default="user",
        required=True,
    )
    use_realization_limit = fields.Boolean(
        string="Use Realization Limit",
    )
    min_realization_limit = fields.Float(
        string="Min. Realization Limit",
    )
    max_realization_limit = fields.Float(
        string="Max. Realization Limit",
        default=100.0,
    )
    score_method = fields.Selection(
        string="Scoring Methods",
        selection=[
            ("higher", "Higher is better"),
            ("lower", "Lower is better"),
            ("range", "Score Ranges"),
        ],
        default="higher",
        required=True,
    )
    use_score_limit = fields.Boolean(
        string="Use Score Limit",
    )
    min_score_limit = fields.Float(
        string="Min. Score Limit",
    )
    max_score_limit = fields.Float(
        string="Max. Score Limit",
        default=100.0,
    )
    score_range_ids = fields.One2many(
        string="Score Ranges",
        comodel_name="kpi_template_line_score_range",
        inverse_name="template_line_id",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void.
#  - result: Return result, the value is float.
result = 0.0""",
        copy=True,
    )
