###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import api, fields, models

class QMSDocumentsSettings(models.TransientModel):
    
    _inherit = "res.config.settings"
    
    enable_workflow_prev_stage = fields.Boolean(
        "Allow jumping back in stages",
        help="Allow managers to jump back in stages."
    )

    @api.model
    def get_values(self):
        res = super(QMSDocumentsSettings, self).get_values()
        get_param = self.env["ir.config_parameter"].sudo().get_param
        
        res.update(
            enable_workflow_prev_stage=get_param("muk_quality_docs.enable_workflow_prev_stage"),
        )
        return res
        
    def set_values(self):
        super(QMSDocumentsSettings, self).set_values()
        
        config = self.env["ir.config_parameter"]
        set_param = config.sudo().set_param
        
        set_param("muk_quality_docs.enable_workflow_prev_stage", self.enable_workflow_prev_stage)
        
        