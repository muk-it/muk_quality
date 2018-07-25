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

odoo.define('muk_quality_docs.DocumentKanbanRenderer', function (require) {
"use strict";

var core = require('web.core');
var ajax = require('web.ajax');
var config = require('web.config');
var session = require('web.session');

var KanbanRenderer = require('web.KanbanRenderer');

var _t = core._t;
var QWeb = core.qweb;

var DocumentKanbanRenderer = KanbanRenderer.extend({
	custom_events: _.extend({}, KanbanRenderer.prototype.custom_events, {
		button_clicked: '_buttonClicked',
    }),
	init: function (parent, state, params) {
		this._super.apply(this, arguments);
		this.kanban_sidebar = {};
	},
	willStart: function () {
		var load_sidebar = this._load_kanban_sidebar_data();
        return $.when(this._super.apply(this, arguments), load_sidebar);
    },
    _renderView: function () {
    	this._renderSidebar();
        return this._super.apply(this, arguments);
    },
    _renderSidebar: function () {
    	this.$el.parent().find('.mk_quality_docs_document_sidebar').remove();
    	if(!config.device.isMobile) {
    		this.sidebar = $("<div>", {
	    		class: "mk_quality_docs_document_sidebar",
	    		html: $(QWeb.render('muk_quality_docs.KanbanDocumentSidebar', {
	                widget: this,
	                data: this.kanban_sidebar,
	            })),
	    	});
    		this.sidebar.find('.mk_quality_docs_sidebar_actions a').on(
    				'click', _.bind(this._on_sidebar_action, this));
    		this.$el.before(this.sidebar);    	
    		var context = this.state.getContext();
	    	if (context.sidebar_action) {
	    		this.sidebar.find("#" + context.sidebar_action).addClass('active');
	    	}
    	}
    },
    _load_kanban_sidebar_data: function() {
    	var self = this;
    	return this._rpc({
            route: '/sidebar/muk_quality_docs_document/kanban',
        }).done(function(result) {
        	self.kanban_sidebar = _.extend({}, self.kanban_sidebar, result);
        });
    },
    _on_sidebar_action: function(ev) {
    	this.trigger_up('sidebar_action', {
    		action: $(ev.currentTarget).data('action'),
    	});
    },
    _buttonClicked: function(ev) {
    	var index = _.findIndex(this.kanban_sidebar.actions, function(action) {
			return action.id === "inbox";
		});
    	if(ev.data.attrs.name === "toggle_read" && index !== -1) {
    		var number = this.kanban_sidebar.actions[index].badge;
    		if(ev.data.record.data.is_read) {
    			this.kanban_sidebar.actions[index].badge = number + 1;
    		} else {
    			this.kanban_sidebar.actions[index].badge = number - 1;
    		}
    	}
    	this._renderSidebar();
    },
});

return DocumentKanbanRenderer;

});
