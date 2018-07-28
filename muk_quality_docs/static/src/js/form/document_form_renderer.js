/**********************************************************************************
* 
*    Copyright (C) 2017 MuK IT GmbH
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as
*    published by the Free Software Foundation, either version 3 of the
*    License, or (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
**********************************************************************************/

odoo.define('muk_quality_docs.DocumentFormRenderer', function (require) {
"use strict";

var core = require('web.core');
var ajax = require('web.ajax');
var config = require('web.config');
var session = require('web.session');

var FormRenderer = require('web.FormRenderer');

var _t = core._t;
var QWeb = core.qweb;

var DocumentFormRenderer = FormRenderer.extend({
	_renderHeaderButton: function (node) {
		if(node.attrs.name === "set_stage_to_next" && this.state.data.next_stage_name) {
			node.attrs.string = _t("Forward to ") + this.state.data.next_stage_name;
		}
		if(node.attrs.name === "set_stage_to_prev" && this.state.data.prev_stage_name) {
			node.attrs.string = _t("Backward to ") + this.state.data.prev_stage_name;
		}
		return this._super(node);
	},
});

return DocumentFormRenderer;

});
