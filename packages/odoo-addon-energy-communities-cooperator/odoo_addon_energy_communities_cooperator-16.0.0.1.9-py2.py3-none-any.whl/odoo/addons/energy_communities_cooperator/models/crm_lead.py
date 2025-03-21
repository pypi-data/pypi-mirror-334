from odoo import models


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    def _get_metadata_values(self):
        metadata = super()._get_metadata_values()
        capital_share_meta_entry = self.metadata_line_ids.filtered(
            lambda meta: meta.key == "ce_member_mandatory_contribution"
        )
        if capital_share_meta_entry:
            metadata["capital_share"] = capital_share_meta_entry.value
        return metadata

    def _get_default_community_wizard(self):
        creation_dict = super()._get_default_community_wizard()

        creation_dict.update(
            {
                "property_cooperator_account": self.env["account.account"]
                .search([("code", "like", "44000%")], limit=1)
                .id,
                "product_share_template": self.env["product.template"]
                .search(
                    [
                        ("is_share", "=", True),
                        ("company_id", "=", creation_dict["parent_id"]),
                    ],
                    limit=1,
                )
                .id,
            }
        )
        return creation_dict
