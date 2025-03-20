# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class MixinKPIAppraisal(models.AbstractModel):
    _name = "mixin.kpi_appraisal"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
    ]
    _description = "Abstract Class for KPI Appraisal"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = False
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    @api.model
    def _get_policy_field(self):
        res = super(MixinKPIAppraisal, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    kpi_id = fields.Many2one(
        string="# KPI",
        comodel_name="mixin.kpi",
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: fields.Date.today(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    line_ids = fields.One2many(
        string="Details",
        comodel_name="mixin.kpi_appraisal_line",
        inverse_name="kpi_appraisal_id",
    )

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        if vals.get("line_ids"):
            new_record.sudo().kpi_id.action_compute_realization()
        return new_record

    def write(self, vals):
        res = super().write(vals)
        if vals.get("line_ids"):
            self.sudo().kpi_id.action_compute_realization()
        return res

    @ssi_decorator.post_confirm_action()
    def _10_approve_data(self):
        self.ensure_one()
        for line in self.line_ids:
            if line._check_realization_limit():
                error_message = _(
                    """
                Context: Realization Limit
                KPI Item: %s
                Realization Value: %s
                Range Limit: %s - %s
                Problem: Realization value is out of range
                Solution: Please change the value of realization
                """
                    % (
                        line.kpi_item_id.name,
                        line.realization,
                        line.min_realization_limit,
                        line.max_realization_limit,
                    )
                )
                raise UserError(error_message)
        self.action_approve_approval()
