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
from odoo.exceptions import MissingError

class QMSDocumentSettings(models.TransientModel):
    
    _inherit = "res.config.settings"
    
    user_can_only_see_viewer_file = fields.Boolean(
        help="User can only see viewer file (if one is provided)."
    )
    
    file_directory = fields.Many2one(
        "muk_dms.directory",
        help="Folder where controlled document files are saved in.",
        ondelete="RESTRICT"
    )
    
    viewer_file_directory = fields.Many2one(
        "muk_dms.directory",
        help="Folder where controlled document viewer files are saved in.",
        ondelete="RESTRICT"
    )
    
    template_file_directory = fields.Many2one(
        "muk_dms.directory",
        help="Folder where controlled document template files are saved in.",
        ondelete="RESTRICT"
    )
    
    template_viewer_file_directory = fields.Many2one(
        "muk_dms.directory",
        help="Folder where controlled document template viewer files are saved in.",
        ondelete="RESTRICT"
    )
    
    @api.model
    def get_values(self):
        res = super(QMSDocumentSettings, self).get_values()
        get_param = self.env["ir.config_parameter"].sudo().get_param
        file_directory_id = int(get_param("muk_quality_docs_dms.file_directory"))
        viewer_file_directory_id = int(get_param("muk_quality_docs_dms.viewer_file_directory"))
        template_file_directory_id = int(get_param("muk_quality_docs_dms.template_file_directory"))
        template_viewer_file_directory_id = int(get_param("muk_quality_docs_dms.template_viewer_file_directory"))
        try:
             if not self.env['muk_dms.directory'].sudo().browse(file_directory_id).exists():
                 file_directory_id = None
        except MissingError:
            file_directory_id = None 
        try:
            if not self.env['muk_dms.directory'].sudo().browse(viewer_file_directory_id).exists():
                viewer_file_directory_id = None
        except MissingError:
            viewer_file_directory_id = None
        try:
            if not self.env['muk_dms.directory'].sudo().browse(template_file_directory_id).exists():
                template_file_directory_id = None
        except MissingError:
            template_file_directory_id = None
        try:
            if not self.env['muk_dms.directory'].sudo().browse(template_viewer_file_directory_id).exists():
                template_viewer_file_directory_id = None
        except MissingError:
            template_viewer_file_directory_id = None
        res.update(
            user_can_only_see_viewer_file=get_param("muk_quality_docs_dms.user_can_only_see_viewer_file"),
            file_directory=file_directory_id,
            viewer_file_directory=viewer_file_directory_id,
            template_file_directory=template_file_directory_id,
            template_viewer_file_directory=template_viewer_file_directory_id,
        )
        return res
        
    def set_values(self):
        super(QMSDocumentSettings, self).set_values()
        
        config = self.env["ir.config_parameter"]
        set_param = config.sudo().set_param
        
        set_param("muk_quality_docs_dms.user_can_only_see_viewer_file", self.user_can_only_see_viewer_file)
        
        if self.file_directory:
            set_param("muk_quality_docs_dms.file_directory", self.file_directory.id)
        else:
            set_param("muk_quality_docs_dms.file_directory", False)
        
        if self.viewer_file_directory:
            set_param("muk_quality_docs_dms.viewer_file_directory", self.viewer_file_directory.id)
        else:
            set_param("muk_quality_docs_dms.viewer_file_directory", False)
        
        if self.template_file_directory:
            set_param("muk_quality_docs_dms.template_file_directory", self.template_file_directory.id)
        else:
            set_param("muk_quality_docs_dms.template_file_directory", False)
        
        if self.template_viewer_file_directory:
            set_param("muk_quality_docs_dms.template_viewer_file_directory", self.template_viewer_file_directory.id)
        else:
            set_param("muk_quality_docs_dms.template_viewer_file_directory", False)
        
        
        
        