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

from odoo import _, http
from odoo.http import request

_logger = logging.getLogger(__name__)

class QualityController(http.Controller):

    @http.route('/sidebar/muk_quality_docs_document/kanban', type='json', auth="user")
    def sidebar_document_kanban(self, **kw):
        return {
            'actions': [
                {   
                    'id': 'all',
                    'tooltip': _("All"),
                    'action': request.env.ref('muk_quality_docs.documents_all_kanban').id,
                    'icon': "fa fa-list",
                    'badge': 0, # Fixme
                    #'badge': request.env['muk_quality_docs.document'].search([], count=True) or 0,
                }, {   
                    'id': 'inbox',
                    'tooltip': _("Inbox"),
                    'action': request.env.ref('muk_quality_docs.documents_unread_kanban').id,
                    'icon': "fa fa-inbox",
                    'badge': 0, # Fixme
                    #'badge': request.env['muk_quality_docs.document'].search([['is_read', '=', False]], count=True) or 0,
                }, {   
                    'id': 'editor',
                    'tooltip': _("Editor"),
                    'action': request.env.ref('muk_quality_docs.documents_editor_kanban').id,
                    'icon': "fa fa-pencil",
                    'badge': 0, # Fixme
                    #'badge': request.env['muk_quality_docs.document'].search([['permission_write', '=', True]], count=True) or 0,
                }, {   
                    'id': 'partner',
                    'tooltip': _("Partner"),
                    'action': request.env.ref('muk_quality_docs.documents_partner_kanban').id,
                    'icon': "fa fa-user",
                    'badge': 0, # Fixme
                    #'badge': request.env['muk_quality_docs.document'].search([['partner_id', '!=', False]], count=True) or 0,
                }
            ]
        }
        
    @http.route('/sidebar/muk_quality_docs_document/list', type='json', auth="user")
    def sidebar_document_list(self, **kw):
        return {
            'actions': [
                {   
                    'id': 'all',
                    'tooltip': _("All"),
                    'action': request.env.ref('muk_quality_docs.documents_all_list').id,
                    'icon': "fa fa-list",
                    'badge': 0, # Fixme
                    #'badge': request.env['muk_quality_docs.document'].search([], count=True) or 0,
                }, {   
                    'id': 'inbox',
                    'tooltip': _("Inbox"),
                    'action': request.env.ref('muk_quality_docs.documents_unread_list').id,
                    'icon': "fa fa-inbox",
                    'badge': 0, # Fixme
                    #'badge': request.env['muk_quality_docs.document'].search([['is_read', '=', False]], count=True) or 0,
                }, {   
                    'id': 'editor',
                    'tooltip': _("Editor"),
                    'action': request.env.ref('muk_quality_docs.documents_editor_list').id,
                    'icon': "fa fa-pencil",
                    'badge': 0, # Fixme
                    #'badge': request.env['muk_quality_docs.document'].search([['permission_write', '=', True]], count=True) or 0,
                }, {   
                    'id': 'partner',
                    'tooltip': _("Partner"),
                    'action': request.env.ref('muk_quality_docs.documents_partner_list').id,
                    'icon': "fa fa-user",
                    'badge': 0, # Fixme
                    #'badge': request.env['muk_quality_docs.document'].search([['partner_id', '!=', False]], count=True) or 0,
                }
            ]
        }