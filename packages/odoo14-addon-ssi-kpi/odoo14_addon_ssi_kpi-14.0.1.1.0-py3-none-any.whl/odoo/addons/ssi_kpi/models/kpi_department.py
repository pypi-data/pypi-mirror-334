# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiDepartment(models.Model):
    _name = "kpi.department"
    _inherit = "mixin.kpi"
    _description = "KPI for Department"

    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    kpi_template_id = fields.Many2one(
        domain="['|',('type', '=', 'department'), ('type', '=', 'both')]"
    )
    line_ids = fields.One2many(
        comodel_name="kpi.department_line",
    )
    appraisal_ids = fields.One2many(
        comodel_name="kpi.department_appraisal",
    )

    def _check_overlap(self):
        self.ensure_one()
        result = True
        criteria = [
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("department_id", "=", self.department_id.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]
        check = self.search_count(criteria)
        if check > 0:
            result = False

        return result


class KpiDepartmentLine(models.Model):
    _name = "kpi.department_line"
    _inherit = "mixin.kpi_line"
    _description = "KPI Line for Department"

    kpi_id = fields.Many2one(
        comodel_name="kpi.department",
    )
    score_range_ids = fields.One2many(
        string="Score Ranges",
        comodel_name="kpi.department_line_score_range",
        inverse_name="kpi_line_id",
    )


class KPIDepartmentLineScoreRange(models.Model):
    _name = "kpi.department_line_score_range"
    _inherit = "mixin.kpi_line_score_range"
    _description = "KPI Line for Department"

    kpi_line_id = fields.Many2one(
        comodel_name="kpi.department_line",
    )


class KPIDepartmentAppraisal(models.Model):
    _name = "kpi.department_appraisal"
    _inherit = "mixin.kpi_appraisal"
    _description = "KPI Appraisal for Department"

    kpi_id = fields.Many2one(
        comodel_name="kpi.department",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        related="kpi_id.department_id",
    )
    line_ids = fields.One2many(
        comodel_name="kpi.department_appraisal_line",
    )


class KPIDepartmentAppraisalLine(models.Model):
    _name = "kpi.department_appraisal_line"
    _inherit = "mixin.kpi_appraisal_line"
    _description = "KPI Appraisal Line for Department"

    kpi_appraisal_id = fields.Many2one(
        comodel_name="kpi.department_appraisal",
    )
    kpi_line_id = fields.Many2one(
        comodel_name="kpi.department_line",
    )
