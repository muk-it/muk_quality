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

import logging

from odoo import _
from odoo import models, fields

_logger = logging.getLogger(__name__)

class Template(models.Model):
    
    _name = "muk_quality_docs.template"
    _description = "QMS Template"
    _inherit = ["mail.thread", "mail.activity.mixin", "muk_security.access_groups"]
    
    #===========================================================================
    # Variables
    #===========================================================================
    
    name = fields.Char(
        required=True,
        track_visibility="onchange",
        translate=True
    )
    
    document_ids = fields.One2many(
        "muk_quality_docs.document",
        "template_id",
        "Documents"
    )
    
    document_name = fields.Char(
        track_visibility="onchange",
        translate=True
    )
    
    document_ref = fields.Char(
        "Document Reference",
        track_visibility="onchange"
    )
    
    document_description = fields.Html(
        translate=True
    )
    
    #===========================================================================
    # Helper Functions
    #===========================================================================
    
    def _get_document_context(self):
        context = {
            "form_view_initial_mode": "edit",
            "force_detailed_view": True,
            "default_template_id": self.id,
        }
        
        if self.document_name:
            context.update({"default_name": self.document_name})
        
        if self.document_ref:
            context.update({"default_ref": self.document_ref})
        
        if self.document_description:
            context.update({"default_description": self.document_description})
            
        if self.groups:
            context.update({"default_groups": self.groups.mapped("id")})
        
        return context
    
    #===========================================================================
    # View Actions
    #===========================================================================
        
    def action_create_document(self):
        context = self._get_document_context()
        
        return {
            "name": _("Create New Document"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "muk_quality_docs.document",
            "target": "current",
            "context": context
        }
    