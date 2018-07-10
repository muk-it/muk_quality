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
import os
import string

from odoo import models, api, fields

from odoo.addons.muk_dms_field.fields import dms_binary

_logger = logging.getLogger(__name__)

class Template(models.Model):
    
    _inherit = "muk_quality_docs.template"
    
    #===========================================================================
    # File Saving Functions
    #===========================================================================
    
    def _get_document_file_name(self):
        try:
            self.env
        except:
            _logger.warning("You are in the wrong Model. Maybe Environment?")
            return False
        valid_chars = "-_.() %s%sÄäÜüÖöß" % (string.ascii_letters, string.digits)
        file_name = "".join(c for c in self.name if c in valid_chars)
        return "{}.{}{}".format(file_name, self.id, self.document_file_ext)
    
    def _get_document_file_directory(self):
        try:
            get_param = self.env["ir.config_parameter"].sudo().get_param
            file_directory = get_param("muk_quality_docs_dms.template_file_directory")
        except:
            try:
                get_param = self["ir.config_parameter"].sudo().get_param
                file_directory = get_param("muk_quality_docs_dms.template_file_directory")
            except:
                file_directory = False
            
        if file_directory:
            return int(file_directory)
        else:
            # raise ValueError("Not-Null-Constraint")
            _logger.warning("You have to provide a directory for QMS template files.")
    
    def _get_document_viewer_file_name(self):
        try:
            self.env
        except:
            _logger.warning("You are in the wrong Model. Maybe Environment?")
            return False
        valid_chars = "-_.() %s%sÄäÜüÖöß" % (string.ascii_letters, string.digits)
        viewer_file_name = "".join(c for c in self.name if c in valid_chars)
        return "{}.{}{}".format(viewer_file_name, self.id, self.document_viewer_file_ext)
    
    def _get_document_viewer_file_directory(self):
        try:
            get_param = self.env["ir.config_parameter"].sudo().get_param
            viewer_file_directory = get_param("muk_quality_docs_dms.template_viewer_file_directory")
        except:
            try:
                get_param = self["ir.config_parameter"].sudo().get_param
                viewer_file_directory = get_param("muk_quality_docs_dms.template_viewer_file_directory")
            except:
                viewer_file_directory = False
            
        if viewer_file_directory:
            return int(viewer_file_directory)
        else:
            # raise ValueError("Not-Null-Constraint")
            _logger.warning("You have to provide a directory for QMS template viewer files.")
    
    #===========================================================================
    # Variables
    #===========================================================================
    
    document_file = dms_binary.DocumentBinary(
        filename=_get_document_file_name,
        directory=_get_document_file_directory
    )
    
    document_file_ext = fields.Char(
        "Document File Extension"
    )
    
    document_file_name = fields.Char(
        compute="_compute_document_file_name",
        inverse="_inverse_document_file_name"
    )
    
    document_viewer_file = dms_binary.DocumentBinary(
        filename=_get_document_viewer_file_name,
        directory=_get_document_viewer_file_directory
    )
    
    document_viewer_file_ext = fields.Char(
        "Document Viewer File Extension"
    )
    
    document_viewer_file_name = fields.Char(
        compute="_compute_document_viewer_file_name",
        inverse="_inverse_document_viewer_file_name"
    )
    
    #===========================================================================
    # Inverse Functions
    #===========================================================================
    
    def _inverse_document_file_name(self):
        for record in self:
            if record.document_file_name:
                file_name, file_extension = os.path.splitext(record.document_file_name)
                record.document_file_ext = file_extension
            else:
                record.document_file_ext = False
    
    def _inverse_document_viewer_file_name(self):
        for record in self:
            if record.document_viewer_file_name:
                viewer_file_name, viewer_file_extension = os.path.splitext(record.document_viewer_file_name)
                record.document_viewer_file_ext = viewer_file_extension
            else:
                record.document_viewer_file_ext = False
    
    #===========================================================================
    # Computed Functions
    #===========================================================================
    
    @api.depends("document_file_ext", "name")
    def _compute_document_file_name(self):
        for record in self:
            if record.document_file_ext and record.name:
                record.document_file_name = record._get_document_file_name()
            else:
                record.document_file_name = False
    
    @api.depends("document_viewer_file_ext", "name")
    def _compute_document_viewer_file_name(self):
        for record in self:
            if record.document_viewer_file_ext and record.name:
                record.document_viewer_file_name = record._get_document_viewer_file_name()
            else:
                record.document_viewer_file_name = False

    #===========================================================================
    # OnChange Functions
    #===========================================================================
    
    @api.onchange("document_file_name")
    def _onchange_file_name(self):
        if self.document_file_name:
            file_name, file_extension = os.path.splitext(self.document_file_name)
            self.document_file_ext = file_extension
        else:
            self.document_file_ext = False
    
    @api.onchange("document_viewer_file_name")
    def _onchange_viewer_file_name(self):
        if self.document_viewer_file_name:
            viewer_file_name, viewer_file_extension = os.path.splitext(self.document_viewer_file_name)
            self.document_viewer_file_ext = viewer_file_extension
        else:
            self.document_viewer_file_ext = False
    
    #===========================================================================
    # Helper Functions
    #===========================================================================
    
    def _get_document_context(self):
        context = super(Template, self)._get_document_context()
        
        if self.document_file_ext:
            context.update({"default_file_ext": self.document_file_ext})
        
        if self.document_file:
            context.update({"default_file": self.document_file})
        
        if self.document_viewer_file_ext:
            context.update({"default_viewer_file_ext": self.document_viewer_file_ext})
        
        if self.document_viewer_file:
            context.update({"default_viewer_file": self.document_viewer_file})
        
        return context
    
    