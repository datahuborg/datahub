define(function(require) {
  var Backbone = require('backbone'),
      Handlebars = require('handlebars'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util')

  // View to render the selected stuff for debugging
  var QueryWhereView = Backbone.View.extend({
    wheretemplate: Handlebars.compile($("#wherelabel-template").html()),
    events: {
      "click .clause button": 'onClose'
    },

    
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'change:basewheres', this.render);
    },

    render: function() {
      this.$el.empty();
      var els = _.map(this.model.get('basewheres'), function(clause, idx) {
        console.log(clause)
        if (clause.sql.trim() == '') return;
        clause = _.clone(clause);
        clause.idx = idx;
        var el = $(this.wheretemplate(clause)).addClass("permanent");
        this.$el.append(el);
      }, this);
      return this;
    },

    onClose: function(ev) {
      var idx = +$(ev.target).data("idx");
      this.model.get('basewheres').splice(idx, 1);
      this.model.trigger("change:basewheres");
    }

  });

  return QueryWhereView;
});
 
