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

import re
import logging

from lxml import etree

from odoo import _
from odoo import models, api, fields
from odoo.tools import html2plaintext
from odoo.exceptions import UserError, AccessError

_logger = logging.getLogger(__name__)

class Document(models.Model):
    
    _name = "muk_quality_docs.document"
    _description = "QMS Document"
    _inherit = ["mail.thread", "mail.activity.mixin", "muk_security.access_groups"]
    _rec_name = "ref_and_name"
    
    #===========================================================================
    # Variables
    #===========================================================================
    
    name = fields.Char(
        required=True,
        track_visibility="onchange",
        translate=True
    )
    
    ref = fields.Char(
        "Reference",
        required=True,
        track_visibility="onchange"
    )
    
    ref_and_name = fields.Char(
        "Full Name",
        compute="_compute_ref_and_name",
        search="_search_ref_and_name"
    )
    
    partner_id = fields.Many2one(
        "res.partner",
        string="Related Partner",
    )
    
    state = fields.Char(
        string="State",
        compute="_compute_state")
    
    stage_id = fields.Many2one(
        "muk_quality_docs.stage",
        string="Stage",
        ondelete="RESTRICT",
        index=True,
        readonly=True,
        default=lambda r: r.env["muk_quality_docs.stage"].get_first_stage(),
        track_visibility="onchange"
    )

    prev_stage_name = fields.Char(
        compute="_compute_stage_names"
    )

    next_stage_name = fields.Char(
        compute="_compute_stage_names"
    )

    has_right_for_prev_stage = fields.Boolean(
        compute="_compute_has_right_for_prev_stage"
    )
    
    has_right_for_next_stage = fields.Boolean(
        compute="_compute_has_right_for_next_stage"
    )
    
    description = fields.Html(
        string='Description', 
        translate=True
    )
    
    summary = fields.Text(
        compute='_compute_summary', 
        string='Summary', 
        store=True)
    
    read_ids = fields.One2many(
        "muk_quality_docs.read",
        "document_id",
        string="Already read by",
        groups="muk_quality_docs.group_muk_quality_docs_manager"
    )
    
    is_read = fields.Boolean(
        compute="_compute_is_read",
        search="_search_is_read"
    )
    
    template_id = fields.Many2one(
        "muk_quality_docs.template",
        "Template",
        groups="muk_quality_docs.group_muk_quality_docs_author"
    )
    
    template_document_id = fields.Many2one(
        "muk_quality_docs.document",
        "Document used as Template",
        groups="muk_quality_docs.group_muk_quality_docs_author"
    )
    
    #===========================================================================
    # View Functions
    #===========================================================================
    
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        # This is needed since tree view wont validate with a js_class attribute
        res = super(Document, self).fields_view_get(view_id, view_type, toolbar, submenu)
        if view_type == 'tree':
            doc = etree.fromstring(res['arch'])
            tree = next(iter( doc.xpath("//tree") or []), None)
            if len(tree):
                tree.set("js_class", "qms_document_list")
                res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
        
    #===========================================================================
    # Computed Functions
    #===========================================================================
    
    @api.depends("name", "ref")
    def _compute_ref_and_name(self):
        for record in self:
            if record.ref and record.name:
                record.ref_and_name = "{} {}".format(record.ref, record.name)
            elif record.ref:
                record.ref_and_name = record.ref
            elif record.name:
                record.ref_and_name = record.name
            else:
                record.ref_and_name = ""
    
    @api.model
    def _depends_state(self):
        return ["is_read"]
    
    @api.depends(_depends_state)
    def _compute_state(self, write=True):
        if write:
            for record in self:
                record.state = "read" if record.is_read else "unread"   
        else:
            self.ensure_one()
            return {'state': "read" if self.is_read else "unread"}         
    
    @api.depends('stage_id')
    def _compute_stage_names(self):
        for record in self:
            record.update({
                'prev_stage_name': record.stage_id.prev_stage_id.name,
                'next_stage_name': record.stage_id.next_stage_id.name})
    
    @api.depends('description')
    def _compute_summary(self):
        for record in self:
            text = html2plaintext(record.description) if record.description else ''
            record.summary = text.strip().replace('*', '').split("\n")[0]
            
    @api.depends("read_ids")
    def _compute_is_read(self):
        for record in self:
            record.is_read = self.env.user.id in record.sudo().read_ids.mapped("user_id.id")
                
    def _compute_has_right_for_prev_stage(self):
        for record in self:
            stage_new = record.stage_id.prev_stage_id
            
            has_right = False
            
            if stage_new:
                get_param = self.env["ir.config_parameter"].sudo().get_param
                enable_workflow_prev_stage = get_param("muk_quality_docs.enable_workflow_prev_stage")
                has_group = self.env.user.has_group("muk_quality_docs.group_muk_quality_docs_manager")
                if enable_workflow_prev_stage and has_group:
                    has_right = True
                elif self.env.user in record.stage_id.prev_stage_group.users:
                    has_right = True
                    
            record.has_right_for_prev_stage = has_right
                
    def _compute_has_right_for_next_stage(self):
        for record in self:
            stage_new = record.stage_id.next_stage_id
            
            has_right = False
            
            if stage_new:
                if self.env.user.has_group("muk_quality_docs.group_muk_quality_docs_manager"):
                    has_right = True
                elif self.env.user in record.stage_id.next_stage_group.users:
                    has_right = True
                    
            record.has_right_for_next_stage = has_right
                
    #===========================================================================
    # Worfklow Functions
    #===========================================================================
    
    @api.multi
    def set_stage_to_next(self):
        for record in self:
        
            if not record.has_right_for_next_stage:
                msg = "You are not allowed to change to the next workflow stage."
                _logger.exception(msg)
                raise UserError(_(msg))
            
            stage_new = record.stage_id.next_stage_id
            
            if not stage_new:
                msg = "This is already the last stage."
                _logger.exception(msg)
                raise UserError(_(msg))
            
            record.sudo().write({
                "stage_id": stage_new.id,
            })
        
    @api.multi
    def set_stage_to_prev(self):
        for record in self:
            
            if not record.has_right_for_prev_stage:
                msg = "You are not allowed to change to the previous workflow stage."
                _logger.exception(msg)
                raise UserError(_(msg))
            
            stage_new = record.stage_id.prev_stage_id
            
            if not stage_new:
                msg = "This is already the first stage."
                _logger.exception(msg)
                raise UserError(_(msg))
            
            record.sudo().write({
                "stage_id": stage_new.id,
            })

    #===========================================================================
    # Toggle Functions
    #===========================================================================
    
    def toggle_read(self):
        if not self.is_read:
            self.env["muk_quality_docs.read"].create({
                "document_id": self.id,
                "user_id": self.env.user.id    
            })
        else:
            self.env["muk_quality_docs.read"].search([
                "&",
                ("document_id", "=", self.id),
                ("user_id", "=", self.env.user.id)
            ]).unlink()

    #===========================================================================
    # Search Functions
    #===========================================================================
    
    @api.multi
    def _search_is_read(self, operator, value):
        if operator == "=":
            records = self.env["muk_quality_docs.read"].sudo().search([("user_id", "=", self.env.user.id)]).mapped("document_id.id")
            return [('id', 'in', records)]
        elif operator == "!=":
            records = self.env["muk_quality_docs.read"].sudo().search([("user_id", "=", self.env.user.id)]).mapped("document_id.id")
            return [('id', 'not in', records)]
        return []
            
    
    @api.multi
    def _search_ref_and_name(self, operator, value):
        records = []
        if operator == "like":
            search_term = re.compile(value) 
            records = self.search([]).filtered(lambda r: value in r.ref_and_name)
        elif operator == "ilike":
            records = self.search([]).filtered(lambda r: value.lower() in r.ref_and_name.lower())
            
        return [('id', 'in', [r.id for r in records])]
               
    #===========================================================================
    # ORM Functions
    #===========================================================================
    
    @api.model
    def create(self, values):
        record = super(Document, self).create(values)
        
        if record.template_id:
            record.with_context({}).post_create_document_from_template()
            
        if record.template_document_id:
            record.with_context({}).post_create_document_from_document()
        
        return record
    
    #===========================================================================
    # Helper Functions
    #===========================================================================
    
    def _get_document_context(self):
        context = {
            "form_view_initial_mode": "edit",
            "force_detailed_view": True,
            "default_template_document_id": self.id,
        }
        
        if self.name:
            context.update({"default_name": self.name})
        
        if self.ref:
            context.update({"default_ref": self.ref})
        
        if self.description:
            context.update({"default_description": self.description})
            
        if self.groups:
            context.update({"default_groups": self.groups.mapped("id")})
        
        return context
    
    #===========================================================================
    # View Actions
    #===========================================================================
        
    def action_create_document_from_document(self):
        context = self._get_document_context()
        
        return {
            "name": _("Create New Document"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "muk_quality_docs.document",
            "target": "current",
            "context": context
        }

    #===========================================================================
    # Post Create Document Functions
    #===========================================================================

    def post_create_document_from_document(self):
        _logger.info("Template Document[id={}]: Document[id={}] created.".format(self.template_document_id.id, self.id))
        return self
    
    def post_create_document_from_template(self):
        _logger.info("Template[id={}]: Document[id={}] created.".format(self.template_id.id, self.id))
        return self
    
    #===========================================================================
    # Security
    #===========================================================================
    
    @api.model
    def _get_suspended_access_ids(self, operation):
        base, model = self._name.split(".")
        sql = '''
            SELECT id
                FROM %s a
                WHERE NOT EXISTS (
                    SELECT *
                    FROM muk_groups_complete_%s_rel r
                    JOIN muk_security_groups g ON g.id = r.gid
                    WHERE r.aid = a.id AND g.perm_%s = true
                );         
            ''' % (self._table, model, operation)
        self.env.cr.execute(sql)
        fetch = self.env.cr.fetchall()
        return len(fetch) > 0 and list(map(lambda x: x[0], fetch)) or []

        
    @api.model
    def _apply_ir_rules(self, query, mode='read'):
        user = self.env.user
        if user.has_group("muk_quality_docs.group_muk_quality_docs_manager"):
            pass
        elif user.has_group("muk_quality_docs.group_muk_quality_docs_author"):
            if mode == "read":
                Stage = self.env["muk_quality_docs.stage"]
                stages = Stage.search([
                    "|",
                     ("has_read_access_for_authors", "=", True), 
                     ("has_write_access_for_authors", "=", True)
                ]).mapped("id")
                if stages:
                    stage_ids = str(stages).replace("[", "(").replace("]", ")")
                    clause = '"muk_quality_docs_document".stage_id IN {}'.format(stage_ids)
                else:
                    clause = '1 != 1'
            
                query.where_clause += [clause]
        elif user.has_group("muk_quality_docs.group_muk_quality_docs_user"):
            if mode == "read":
                Stage = self.env["muk_quality_docs.stage"]
                stages = Stage.search([("has_read_access_for_users", "=", True)]).mapped("id")
                if stages:
                    stage_ids = str(stages).replace("[", "(").replace("]", ")")
                    clause = '"muk_quality_docs_document".stage_id IN {}'.format(stage_ids)
                else:
                    clause = '1 != 1'
            
                query.where_clause += [clause]
            
        return super(Document, self)._apply_ir_rules(query, mode)
    
    @api.multi
    def check_access_rule(self, operation):
        value = super(Document, self).check_access_rule(operation)
        user = self.env.user

        if operation == "write":
            if user.id == 1:
                pass
            elif user.has_group("muk_quality_docs.group_muk_quality_docs_manager"):
                ids = self.filtered("stage_id.has_write_access_for_managers").mapped("id")
                if len(ids) != len(self):
                    raise AccessError(_("Managers are not allowed to write on this stage!"))
            elif user.has_group("muk_quality_docs.group_muk_quality_docs_author"):
                ids = self.filtered("stage_id.has_write_access_for_authors").mapped("id")
                if len(ids) != len(self):
                    raise AccessError(_("Authors are not allowed to write on this stage!"))
        
        return value
