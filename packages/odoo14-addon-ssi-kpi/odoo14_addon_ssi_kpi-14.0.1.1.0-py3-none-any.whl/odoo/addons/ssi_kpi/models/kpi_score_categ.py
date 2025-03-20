# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class KpiScoreCateg(models.Model):
    _name = "kpi_score_categ"
    _inherit = ["mixin.master_data"]
    _description = "KPI Score Category"

    code = fields.Char(
        default="/",
    )
    range_ids = fields.One2many(
        string="Range(s)",
        comodel_name="kpi_score_categ_range",
        inverse_name="score_categ_id",
    )

    @api.depends(
        "range_ids",
        "range_ids.min_value",
    )
    def _compute_min_range_value_id(self):
        for record in self:
            min_score_id = False
            if record.range_ids:
                min_score = min(record.range_ids.mapped("min_value"))
                min_score_id = record.range_ids.filtered(
                    lambda x: x.min_value == min_score
                )[0]
                if min_score_id:
                    min_score_id = min_score_id.id
            record.min_range_value_id = min_score_id

    min_range_value_id = fields.Many2one(
        string="Min. Range Value",
        comodel_name="kpi_score_categ_range",
        compute="_compute_min_range_value_id",
        readonly=True,
        store=True,
    )

    @api.depends(
        "range_ids",
        "range_ids.max_value",
    )
    def _compute_max_range_value_id(self):
        for record in self:
            max_score_id = False
            if record.range_ids:
                max_score = max(record.range_ids.mapped("max_value"))
                max_score_id = record.range_ids.filtered(
                    lambda x: x.max_value == max_score
                )[0]
                if max_score_id:
                    max_score_id = max_score_id.id
            record.max_range_value_id = max_score_id

    max_range_value_id = fields.Many2one(
        string="Max. Range Value",
        comodel_name="kpi_score_categ_range",
        compute="_compute_max_range_value_id",
        readonly=True,
        store=True,
    )

    def _get_range_result(self, final_score):
        self.ensure_one()
        result = ""
        if final_score < self.min_range_value_id.min_value:
            result = self.min_range_value_id.categ_range_value_id.name
        elif final_score > self.max_range_value_id.max_value:
            result = self.max_range_value_id.categ_range_value_id.name
        else:
            criteria = [
                ("min_value", "<=", final_score),
                ("max_value", ">=", final_score),
            ]
            score_range_ids = self.range_ids.search(criteria, limit=1)
            if score_range_ids:
                result = score_range_ids.categ_range_value_id.name
        return result
