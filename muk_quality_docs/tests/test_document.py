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

import os
import logging
import unittest

from odoo import fields
from odoo.tests import common
from odoo.exceptions import AccessError
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class DocumentTestCase(common.TransactionCase):
    at_install = False
    post_install = True
            
    def test_security_without_groups(self):
        data = self.TestData(self.env)
        for user_id in data.user_ids:
            document_id = self.env["muk_quality_docs.document"].create({
                "name": "Test Document {}".format(user_id.name),
                "ref": "TD-{}".format(user_id.id),
                "stage_id": data.stage_ids[0].id
            })
            for stage_id in data.stage_ids:
                self.assertEqual(stage_id, document_id.stage_id)
                
                test_description = "User={};Document={};Stage={}".format(
                    user_id.name, document_id.id, stage_id.name
                )

                _logger.info(test_description)
                
                has_read_in_stage = False
                has_write_in_stage = False
                
                if user_id.has_group("muk_quality_docs.group_muk_quality_docs_manager"):
                    has_read_in_stage = True
                    has_write_in_stage = stage_id.has_write_access_for_managers
                elif user_id.has_group("muk_quality_docs.group_muk_quality_docs_author"):
                    has_read_in_stage = stage_id.has_read_access_for_authors | stage_id.has_write_access_for_authors
                    has_write_in_stage = stage_id.has_write_access_for_authors
                elif user_id.has_group("muk_quality_docs.group_muk_quality_docs_user"):
                    has_read_in_stage = stage_id.has_read_access_for_users
                    has_write_in_stage = False
                    
                _logger.info("has_read_in_stage={}".format(has_read_in_stage))
                _logger.info("has_write_in_stage={}".format(has_write_in_stage))
                    
                    
                # Test no group set
                _logger.info("Testing read without groups:")
                if has_read_in_stage:
                    self.assertTrue(len(document_id.sudo(user=user_id.id).read()) > 0)
                else:
                    with self.assertRaises(AccessError):
                        document_id.sudo(user=user_id.id).read()
                _logger.info("Done!")
                        
                _logger.info("Testing write without groups:")
                if has_write_in_stage:
                    document_id.sudo(user=user_id.id).write({"name": test_description})
                    self.assertEqual(document_id.name, test_description)
                else:
                    with self.assertRaises(AccessError):
                        document_id.sudo(user=user_id.id).write({"name": test_description})
                _logger.info("Done!")
                         
                if document_id.stage_id != data.stage_ids[-1]:
                    document_id.set_stage_to_next()
                else:
                    document_id.sudo().write({"stage_id": data.stage_ids[0].id})
                    
            
    def test_security_with_groups(self):
        data = self.TestData(self.env)
        for user_id in data.user_ids:
            document_id = self.env["muk_quality_docs.document"].create({
                "name": "Test Document {}".format(user_id.name),
                "ref": "TD-{}".format(user_id.id),
                "stage_id": data.stage_ids[0].id
            })
            for stage_id in data.stage_ids:
                self.assertEqual(stage_id, document_id.stage_id)
                
                test_description = "User={};Document={};Stage={}".format(
                    user_id.name, document_id.id, stage_id.name
                )

                _logger.info(test_description)
                
                has_read_in_stage = False
                has_write_in_stage = False
                
                if user_id.has_group("muk_quality_docs.group_muk_quality_docs_manager"):
                    has_read_in_stage = True
                    has_write_in_stage = stage_id.has_write_access_for_managers
                elif user_id.has_group("muk_quality_docs.group_muk_quality_docs_author"):
                    has_read_in_stage = stage_id.has_read_access_for_authors | stage_id.has_write_access_for_authors
                    has_write_in_stage = stage_id.has_write_access_for_authors
                elif user_id.has_group("muk_quality_docs.group_muk_quality_docs_user"):
                    has_read_in_stage = stage_id.has_read_access_for_users
                    has_write_in_stage = False
                    
                _logger.info("has_read_in_stage={}".format(has_read_in_stage))
                _logger.info("has_write_in_stage={}".format(has_write_in_stage))
                         
                # Test wrong group set READ
                group = self.env["muk_security.groups"].create({
                    "name": "WRONG READ",
                    "perm_read": True,
                })
                group.explicit_users = data.user_ids - user_id
                document_id.groups = group
                with self.assertRaises(AccessError):
                    if len(document_id.sudo(user=user_id.id).read()) == 0:
                        raise AccessError("Fields couldn't be accessed.")
                group.unlink()
                
                # Test right group set READ
                group = self.env["muk_security.groups"].create({
                    "name": "RIGHT READ",
                    "perm_read": True,
                })
                group.explicit_users = user_id
                document_id.groups = group
                if has_read_in_stage:
                    self.assertTrue(len(document_id.sudo(user=user_id.id).read()) > 0)
                else:
                    with self.assertRaises(AccessError):
                        document_id.sudo(user=user_id.id).read()
                group.unlink()
                               
                # Test wrong group set WRITE
                group = self.env["muk_security.groups"].create({
                    "name": "WRONG WRITE",
                    "perm_write": True,
                })
                group.explicit_users = data.user_ids - user_id
                document_id.groups = group
                with self.assertRaises(AccessError):
                    document_id.sudo(user=user_id.id).write({"name": test_description})
                group.unlink()
                
                # Test right group set WRITE
                group = self.env["muk_security.groups"].create({
                    "name": "RIGHT WRITE",
                    "perm_write": True,
                })
                group.explicit_users = user_id
                document_id.groups = group
                
                if has_write_in_stage:
                    document_id.sudo(user=user_id.id).write({"name": test_description})
                    self.assertEqual(document_id.name, test_description)
                else:
                    with self.assertRaises(AccessError):
                        document_id.sudo(user=user_id.id).write({"name": test_description})
                group.unlink()
                               
                # Test no read group set with write set
                group = self.env["muk_security.groups"].create({
                    "name": "WRONG WRITE",
                    "perm_write": True,
                })
                group.explicit_users = data.user_ids - user_id
                document_id.groups = group
                
                if has_read_in_stage:
                    self.assertTrue(len(document_id.sudo(user=user_id.id).read()) > 0)
                else:
                    with self.assertRaises(AccessError):
                        if(len(document_id.sudo(user=user_id.id).read()) == 0):
                            raise AccessError("No read right for stage")
                        
                group.perm_read = True
                
                with self.assertRaises(AccessError):
                    if(len(document_id.sudo(user=user_id.id).read()) == 0):
                        raise AccessError("No read right for stage")
                    
                group.unlink()
                    
                if document_id.stage_id != data.stage_ids[-1]:
                    document_id.set_stage_to_next()
                else:
                    document_id.sudo().write({"stage_id": data.stage_ids[0].id})
                    
    @unittest.skipIf(os.environ.get('TRAVIS', False), "Skipped for Travis CI")
    def test_workflow_security(self):
        data = self.TestData(self.env)
        for user_id in data.user_ids:
            document_id = self.env["muk_quality_docs.document"].create({
                "name": "Test Document {}".format(user_id.name),
                "ref": "TD-{}".format(user_id.id),
                "stage_id": data.stage_ids[0].id
            })
            
            test_description = "Test=Workflow;User={};Document={};Stage={}".format(
                user_id.name, document_id.id, document_id.stage_id.name
            )

            _logger.info(test_description)
            
            data.stage_ids.write({
                "has_read_access_for_users": True,
                "has_read_access_for_authors": True
            })
            
            # Test no stage set
            document_id.stage_id.next_stage_group = False
                
            if user_id.has_group("muk_quality_docs.group_muk_quality_docs_manager"):
                has_right = True
            elif user_id.has_group("muk_quality_docs.group_muk_quality_docs_author"):
                has_right = False
            elif user_id.has_group("muk_quality_docs.group_muk_quality_docs_user"):
                has_right = False
            else:
                has_right = False
            
            
            if(has_right):
                document_id.sudo(user=user_id.id).set_stage_to_next()
            else:
                with self.assertRaises(UserError):
                    document_id.sudo(user=user_id.id).set_stage_to_next()
                               
            # Test wrong group
            group = self.env["muk_quality_docs.groups"].create({
                "name": "WORKFLOW MANAGER",
            })
            group.explicit_users = data.user_ids - user_id
            document_id.stage_id.next_stage_group = group
            if not has_right:
                with self.assertRaises(UserError):
                    document_id.sudo(user=user_id.id).set_stage_to_next()
            else:
                document_id.sudo(user=user_id.id).set_stage_to_next()
            group.unlink()
            
            # Test right group
            group = self.env["muk_quality_docs.groups"].create({
                "name": "WORKFLOW MANAGER",
            })
            group.explicit_users = user_id
            document_id.stage_id.next_stage_group = group
            document_id.sudo(user=user_id.id).set_stage_to_next()
            group.unlink()
    
    class TestData():
        def __init__(self, env):
            self.manager = env.ref("muk_quality_docs.manager_demo")
            self.author = env.ref("muk_quality_docs.author_demo")
            self.user = env.ref("base.user_demo")
            
            self.user_ids = self.manager | self.author | self.user
            
            self.stage_ids = env["muk_quality_docs.stage"].search([("sequence", ">", 1000)])
    