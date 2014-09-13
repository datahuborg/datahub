define(function(require) {
  var Backbone = require('backbone'),
      Handlebars = require('handlebars'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util');


  var ScorpionResultView = Backbone.View.extend({
    template: Handlebars.compile($("#scorpion-result-template").html()),
    events: {
      "click .equiv-toggle":  "onToggle",
      "click .filter-clause": "onClick"
    },

    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
    },

    onClick: function() {
      this.trigger("click", this);
    },

    onToggle: function() {
      var toggle = this.$(".equiv-toggle"),
          equiv = this.$(".equiv-clauses");

      if (toggle.text() == 'show rules in cluster') {
        toggle.text('hide');
        equiv.show();
      } else {
        toggle.text('show rules in cluster');
        equiv.hide();
      }
    },

    render: function() {
      var _this = this,
          json = this.model.toJSON();

      this.$el.html(this.template(json));

      this.$('.filter-clause').hover(
        function() { _this.trigger('selected', _this.model); },
        function() { _this.trigger('unselected', _this.model); }
      );

      return this;
    }

  });

  return ScorpionResultView;
})

