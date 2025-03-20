# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinKPILine(models.AbstractModel):
    _name = "mixin.kpi_line"
    _description = "Abstract Class for KPI Line"

    kpi_id = fields.Many2one(
        string="# KPI",
        comodel_name="mixin.kpi",
        required=True,
        ondelete="cascade",
    )
    kpi_item_id = fields.Many2one(
        string="Item",
        comodel_name="kpi_item",
        required=True,
    )
    weight = fields.Float(
        string="Weight(%)",
    )
    target = fields.Float(
        string="Target",
    )

    @api.depends(
        "kpi_id",
        "kpi_id.appraisal_ids",
        "realization_method",
    )
    def _compute_realization(self):
        for record in self:
            if record.realization_method == "user":
                record.realization = record._get_realization_appraisal()
            else:
                record.realization = record._get_realization_python()

    def _get_realization_appraisal(self):
        self.ensure_one()
        result = 0
        obj_kpi_appraisal_line = self.env[self.kpi_id.appraisal_ids.line_ids._name]
        criteria = [
            ("kpi_appraisal_id.kpi_id", "=", self.kpi_id.id),
            ("kpi_item_id", "=", self.kpi_item_id.id),
        ]
        appraisal_line_ids = obj_kpi_appraisal_line.search(criteria)
        avg = len(self.kpi_id.appraisal_ids.ids)
        if appraisal_line_ids:
            for appraisal_line in appraisal_line_ids:
                result += appraisal_line.realization
            result = result / avg
        return result

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _get_realization_python(self):
        self.ensure_one()
        res = False
        localdict = self._get_localdict()
        try:
            safe_eval(self.python_code, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

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
    realization = fields.Float(
        string="Realization",
        compute="_compute_realization",
        compute_sudo=True,
        store=True,
    )

    @api.depends(
        "score_method",
        "realization",
        "target",
    )
    def _compute_score(self):
        for record in self:
            if record.realization:
                record.score = record._get_score()
                if record.use_score_limit:
                    if record.realization > record.target:
                        record.score = record._get_score_limit(record.score)
            else:
                if record.score_method == "lower":
                    if record.use_score_limit:
                        record.score = record.max_score_limit
                    else:
                        record.score = 100
                else:
                    record.score = 0.0

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
    score = fields.Float(
        string="Score",
        compute="_compute_score",
        compute_sudo=True,
        store=True,
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
        comodel_name="mixin.kpi_line_score_range",
        inverse_name="kpi_line_id",
    )

    @api.depends(
        "score",
    )
    def _compute_final_score(self):
        for record in self:
            if record.score:
                if record.score_method == "range":
                    max_score = record._get_max_score_range()
                    record.final_score = (
                        (record.score / max_score) * (record.weight / 100)
                    ) * 100
                else:
                    record.final_score = record.score * (record.weight / 100)
            else:
                record.final_score = 0.0

    final_score = fields.Float(
        string="Final Score(%)",
        compute="_compute_final_score",
        compute_sudo=True,
        store=True,
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

    def _get_score(self):
        self.ensure_one()
        if self.score_method == "higher":
            score = (self.realization / self.target) * 100
        elif self.score_method == "lower":
            score = (self.target / self.realization) * 100
        else:
            score = self._get_score_range(self.realization)
        return score

    def _get_score_limit(self, score):
        self.ensure_one()
        # if self.score_method == "higher":
        #     score = (self.realization / self.target) * self.max_score_limit
        # elif self.score_method == "lower":
        #     score = (self.target / self.realization) * self.max_score_limit
        # else:
        #     score = self._get_score_range(self.realization)
        if score < self.min_score_limit:
            score = self.min_score_limit
        elif score > self.max_score_limit:
            score = self.max_score_limit
        else:
            pass
        return score

    def _get_score_range(self, realization):
        self.ensure_one()
        score = 0.0
        obj_score_range = self.env[self.score_range_ids._name]
        criteria = [
            ("kpi_line_id", "=", self.id),
            ("min_value", "<=", realization),
            ("max_value", ">=", realization),
        ]
        score_range_ids = obj_score_range.search(criteria, limit=1)
        if score_range_ids:
            score = score_range_ids.score
        return score

    def _get_max_score_range(self):
        self.ensure_one()
        max_score = 0.0
        obj_score_range = self.env[self.score_range_ids._name]
        criteria = [
            ("kpi_line_id", "=", self.id),
        ]
        score_range_ids = obj_score_range.search(criteria)
        if score_range_ids:
            max_score = max(score_range_ids.mapped("score"))
        return max_score
