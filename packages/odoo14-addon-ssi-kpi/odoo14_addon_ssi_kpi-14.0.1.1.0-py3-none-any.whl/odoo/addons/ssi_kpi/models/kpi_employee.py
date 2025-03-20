# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class KpiEmployee(models.Model):
    _name = "kpi.employee"
    _inherit = "mixin.kpi"
    _description = "KPI for Employee"

    @api.model
    def _default_employee_id(self):
        employees = self.env.user.employee_ids
        if len(employees) > 0:
            return employees[0].id

    kpi_template_id = fields.Many2one(
        domain="['|',('type', '=', 'employee'), ('type', '=', 'both')]"
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        default=lambda self: self._default_employee_id(),
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    line_ids = fields.One2many(
        comodel_name="kpi.employee_line",
    )
    appraisal_ids = fields.One2many(
        comodel_name="kpi.employee_appraisal",
    )

    def _check_overlap(self):
        self.ensure_one()
        result = True
        criteria = [
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("employee_id", "=", self.employee_id.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]
        check = self.search_count(criteria)
        if check > 0:
            result = False

        return result


class KPIEmployeeLine(models.Model):
    _name = "kpi.employee_line"
    _inherit = "mixin.kpi_line"
    _description = "KPI Line for Employee"

    kpi_id = fields.Many2one(
        comodel_name="kpi.employee",
    )
    score_range_ids = fields.One2many(
        string="Score Ranges",
        comodel_name="kpi.employee_line_score_range",
        inverse_name="kpi_line_id",
    )


class KPIEmployeeLineScoreRange(models.Model):
    _name = "kpi.employee_line_score_range"
    _inherit = "mixin.kpi_line_score_range"
    _description = "KPI Line for Employee"

    kpi_line_id = fields.Many2one(
        comodel_name="kpi.employee_line",
    )


class KPIEmployeeAppraisal(models.Model):
    _name = "kpi.employee_appraisal"
    _inherit = "mixin.kpi_appraisal"
    _description = "KPI Appraisal for Employee"

    kpi_id = fields.Many2one(
        comodel_name="kpi.employee",
    )
    employee_id = fields.Many2one(
        string="Employee", comodel_name="hr.employee", related="kpi_id.employee_id"
    )
    line_ids = fields.One2many(
        comodel_name="kpi.employee_appraisal_line",
    )


class KPIEmployeeAppraisalLine(models.Model):
    _name = "kpi.employee_appraisal_line"
    _inherit = "mixin.kpi_appraisal_line"
    _description = "KPI Appraisal Line for Employee"

    kpi_appraisal_id = fields.Many2one(
        comodel_name="kpi.employee_appraisal",
    )
    kpi_line_id = fields.Many2one(
        comodel_name="kpi.employee_line",
    )
