# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MixinKPILineScoreRange(models.AbstractModel):
    _name = "mixin.kpi_line_score_range"
    _rec_name = "kpi_line_id"
    _description = "Abstract Class KPI Line Score Range"

    kpi_line_id = fields.Many2one(string="#KPI Line", comodel_name="mixin.kpi_line")
    min_value = fields.Float(
        string="Min. Value",
        required=True,
        default=0,
    )
    max_value = fields.Float(
        string="Max. Value",
        required=True,
        default=0,
    )
    score = fields.Float(
        string="Score",
        required=True,
        default=0,
    )
