###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK QMS Documents 
#    (see https://mukit.at).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class Read(models.Model):
    
    _name = "muk_quality_docs.read"
    _description = "QMS Reading Information"
    
    #===========================================================================
    # Variables
    #===========================================================================
    
    user_id = fields.Many2one(
        "res.users",
        required=True,
        ondelete="cascade"
    )
    
    document_id = fields.Many2one(
        "muk_quality_docs.document",
        required=True,
        ondelete="cascade"
    )