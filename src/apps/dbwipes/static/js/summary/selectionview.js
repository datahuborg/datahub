define(function(require) {
  var Backbone = require('backbone'),
      Handlebars = require('handlebars'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util')

  // View to render the selected stuff for debugging
  var SelectionView = Backbone.View.extend({
    errtemplate: Handlebars.compile($("#wherelabel-template").html()),
    events: {
      "click .clause button": 'onClose'
    },

    initialize: function() {
      this.listenTo(this.model, 'change:selection', this.render);
    },

    render: function() {
      var sel = this.model.get('selection'),
          type = this.model.get('type'),
          vals = _.keys(sel);

      if (vals.length == 0) {
        this.clear();
        return this;
      }
      var sql = util.negateClause(this.model.toSQLWhere());
      this.$el.html(this.errtemplate({sql: sql}));
      this.$(".clause").addClass("temporary");
      this.$el.show()
      return this;
    },

    clear: function() {
      this.$el.hide();
      return this;
    },

    onClose: function() {
      this.model.set('selection', []);
      this.model.trigger('clearScorpionSelection');
    }


  })

  return SelectionView;
})
