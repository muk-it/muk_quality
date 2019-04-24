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

odoo.define('muk_quality_docs_dms.DocumentKanbanRenderer', function (require) {
"use strict";

var core = require('web.core');
var ajax = require('web.ajax');
var config = require('web.config');
var session = require('web.session');

var DocumentKanbanRenderer = require('muk_quality_docs.DocumentKanbanRenderer');

var _t = core._t;
var QWeb = core.qweb;

DocumentKanbanRenderer.include({
	events: _.extend({}, DocumentKanbanRenderer.prototype.events, {
		'click .mk_quality_docs_preview': '_preview',
    }),
    _preview: function(ev) {
    	ev.stopPropagation();
    	ev.preventDefault();
		var filename = $(ev.currentTarget).data('filename');
    	this.trigger_up('show_preview', {
    		url: '/web/content?' + $.param({
    			'model': "muk_quality_docs.document",
                'id': $(ev.currentTarget).data('id'),
                'field': $(ev.currentTarget).data('field'),
                'filename_field': $(ev.currentTarget).data('filename_field'),
                'filename': filename,
                'download': true,
            }),
            mimetype: false,
            extension: filename.split('.').pop(),
            filename, filename,
    	});
    }
});

});
