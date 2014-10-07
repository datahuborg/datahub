// CStatsView
define(function(require) {
  var $ = require("jquery"),
      CStatView = require('summary/cstatview'),
      Backbone = require('backbone');

  return Backbone.View.extend({

    initialize: function() {
      this.listenTo(this.collection, 'add', this.addOne);
      this.listenTo(this.collection, 'reset', this.onReset);
      $("#facet-togglecheckall").click(this.toggleChecks.bind(this));
    },

    toggleChecks: function() {
      var btn = $("#facet-togglecheckall");
      var bchecked = false;
      if (btn.attr('state') == 'checked') {
        btn.text("check all");
        btn.attr('state', 'unchecked');
        bchecked = false;
      } else {
        btn.text('uncheck all');
        btn.attr('state', 'checked');
        bchecked = true;
      }


      this.$("input.errcol").each(function(idx, el) {
        el.checked = bchecked;
      });
    },

    onReset: function() {
      this.$el.empty();
      this.collection.each(this.addOne.bind(this));
    },

    addOne: function(model) {
      var _this = this;
      var view = new CStatView({model: model});
      var vel = view.render().el;
      view.on("dragStart", _.bind(this.trigger, this, "dragStart"));
      view.on("drag",      _.bind(this.trigger, this, "drag"));
      view.on("dragEnd",   _.bind(this.trigger, this, "dragEnd"));


      this.$el.append(vel);
    }
  });
});

