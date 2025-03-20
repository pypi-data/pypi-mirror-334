# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KPIScoreCategRangeValue(models.Model):
    _name = "kpi_score_categ_range_value"
    _inherit = ["mixin.master_data"]
    _description = "KPI Score Category Value"

    name = fields.Char(
        string="Value",
    )
    code = fields.Char(
        default="/",
    )
