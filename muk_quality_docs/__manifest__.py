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

{
    "name": "MuK QMS Documents",
    "summary": """Quality Management System""",
    "version": "11.0.1.1.15",
    "author": "MuK IT",
    "category": "Document Management",
    "license": "AGPL-3",
    "website": "http://www.mukit.at",
    "live_test_url": "https://demo.mukit.at/web/login",
    "depends": [
        "mail",
        "muk_security",
        "muk_web_client_refresh",
        "muk_automation_extension"
    ],
    "contributors": [
        "Kerrim Abdelhamed <kerrim.abdelhamed@mukit.at>",
        "Mathias Markl <mathias.markl@mukit.at>",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "template/assets.xml",
        "views/document_view.xml",
        "views/stage_view.xml",
        "views/groups_view.xml",
        "views/template_view.xml",
        "views/res_config_view.xml",
        "views/menu.xml",
        "data/stages.xml",
        "data/refresh_actions.xml",
    ],
    "demo": [
        "demo/document_demo.xml",
        "demo/template_demo.xml",
        "demo/read_demo.xml",
        "demo/user_demo.xml",
        "demo/muk_quality_docs.stage.csv"
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    "images": [
        'static/description/banner.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "sequence": 100,
    "installable": True,
    "auto_install": False,
    "application": True,
}
