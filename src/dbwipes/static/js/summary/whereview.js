define(function(require) {
  var Backbone = require('backbone'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      SelectionView = require('summary/selectionview');


  var WhereView = Backbone.View.extend({
    initialize: function() {
      var collection = this.collection;
      this.listenTo(collection, 'add', this.addOne);
      this.listenTo(collection, 'reset', this.onReset);
      this.listenTo(collection, 'change:selection', this.render);
    },

    onReset: function() {
      this.render();
      return this;
    },

    addOne: function(model) {
      var view = new SelectionView({model: model});
      var vel = view.render().el;
      this.$el.append(vel);
    },

    render: function() {
      this.$el.empty();
      this.collection.each(this.addOne.bind(this));
      return this;
    }


  })

  return WhereView
});
