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

from odoo import models, api, fields

_logger = logging.getLogger(__name__)

class Stage(models.Model):
    
    _name = "muk_quality_docs.stage"
    _inherit = ['mail.thread']
    _description = "QMS Stage"
    _order = "sequence"
    _sql_constraints = [
        ('sequence_unique', 'unique(sequence)', 'Please enter a unique sequence.'),
    ]
    
    #===========================================================================
    # Variables
    #===========================================================================
    
    name = fields.Char(
        required=True,
        translate=True
    )
    
    document_ids = fields.One2many(
        "muk_quality_docs.document",
        "stage_id",
    )
    
    sequence = fields.Integer(
        required=True,
        copy=False
    )
    
    next_stage_id = fields.Many2one(
        "muk_quality_docs.stage",
        compute="_compute_next_stage_id"
    )
    
    prev_stage_id = fields.Many2one(
        "muk_quality_docs.stage",
        compute="_compute_prev_stage_id"
    )
    
    next_stage_group = fields.Many2one('muk_quality_docs.groups')
    prev_stage_group = fields.Many2one('muk_quality_docs.groups')
    
    has_read_access_for_users = fields.Boolean()
    has_read_access_for_authors = fields.Boolean()
    
    has_write_access_for_authors = fields.Boolean()
    has_write_access_for_managers = fields.Boolean()
    
    #===========================================================================
    # Computed Functions
    #===========================================================================
    
    def _compute_next_stage_id(self):
        for record in self:
            next_stage = self.sudo().search([("sequence", ">", record.sequence)])
            if next_stage:
                record.next_stage_id = next_stage[0]
            else:
                record.next_stage_id = False
    
    def _compute_prev_stage_id(self):
        for record in self:
            prev_stage = self.sudo().search([("sequence", "<", record.sequence)])
            if prev_stage:
                record.prev_stage_id = prev_stage[-1]
            else:
                record.prev_stage_id = False
                
    #===========================================================================
    # Global Helper Functions
    #===========================================================================
    
    @api.model
    def get_first_stage(self):
        records = self.search([])
        if records:
            return records[0]
        else:
            return False
    
    @api.model
    def get_last_stage(self):
        records = self.search([])
        if records:
            return records[-1]
        else:
            return False
    
    