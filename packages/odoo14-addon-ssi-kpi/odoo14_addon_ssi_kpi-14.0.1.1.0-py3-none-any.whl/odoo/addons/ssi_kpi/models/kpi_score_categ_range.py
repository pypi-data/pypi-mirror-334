# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KPIScoreCategRange(models.Model):
    _name = "kpi_score_categ_range"
    _rec_name = "categ_range_value_id"
    _description = "KPI Score Category Range"
    _order = "min_value ASC"

    score_categ_id = fields.Many2one(
        string="#Score Category", comodel_name="kpi_score_categ"
    )
    min_value = fields.Float(
        string="Min.",
        required=True,
        default=0,
    )
    max_value = fields.Float(
        string="Max.",
        required=True,
        default=0,
    )
    categ_range_value_id = fields.Many2one(
        string="Value", comodel_name="kpi_score_categ_range_value"
    )
