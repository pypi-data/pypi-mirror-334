# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MixinKpiAppraisalLine(models.AbstractModel):
    _name = "mixin.kpi_appraisal_line"
    _description = "Abstract Class for KPI Apprasial Line"

    kpi_appraisal_id = fields.Many2one(
        string="# KPI Apprasial",
        comodel_name="mixin.kpi_appraisal",
        required=True,
        ondelete="cascade",
    )
    kpi_line_id = fields.Many2one(
        string="# KPI Line",
        comodel_name="mixin.kpi_line",
    )
    kpi_item_id = fields.Many2one(
        string="Item",
        related="kpi_line_id.kpi_item_id",
    )
    weight = fields.Float(
        string="Weight(%)",
        related="kpi_line_id.weight",
    )
    target = fields.Float(
        string="Target",
        related="kpi_line_id.target",
    )
    score_method = fields.Selection(
        string="Score Method",
        related="kpi_line_id.score_method",
    )
    use_score_limit = fields.Boolean(
        string="Use Score Limit",
        related="kpi_line_id.use_score_limit",
    )
    min_score_limit = fields.Float(
        string="Min. Score Limit",
        related="kpi_line_id.min_score_limit",
    )
    max_score_limit = fields.Float(
        string="Max. Score Limit",
        related="kpi_line_id.max_score_limit",
    )
    use_realization_limit = fields.Boolean(
        string="Use Realization Limit",
        related="kpi_line_id.use_realization_limit",
    )
    min_realization_limit = fields.Float(
        string="Min. Realization Limit",
        related="kpi_line_id.min_realization_limit",
    )
    max_realization_limit = fields.Float(
        string="Max. Realization Limit",
        related="kpi_line_id.max_realization_limit",
    )
    realization = fields.Float(
        string="Realization",
        required=True,
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        related="kpi_appraisal_id.state",
    )

    def _check_realization_limit(self):
        self.ensure_one()
        check = False
        if self.use_realization_limit:
            if (
                self.realization < self.min_realization_limit
                or self.realization > self.max_realization_limit
            ):
                check = True
        return check
