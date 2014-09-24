define(function(require) {
  var Backbone = require('backbone'),
      Handlebars = require('handlebars'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util'),
      ScorpionResult = require('summary/scorpionresult'),
      ScorpionResultView = require('summary/scorpionresultview'),
      Query = require('summary/query');


  var ScorpionResultsView = Backbone.View.extend({
    template: Handlebars.compile($("#scorpion-results-template").html()),

    initialize: function(attrs) {
      this.state = {
        locked: null,  // null = base results, int = scorpion result views
        where: null,   // global where object
        query: null
      };
      _.extend(this.state, attrs);


      this.listenTo(this.collection, 'add', this.addTo);
      this.listenTo(this.collection, 'reset', this.reset);
      this.listenTo(this.state.query, 'change:db', this.clear);
      this.listenTo(this.state.query, 'change:table', this.clear);

    },

    render: function() {
      this.$el.html(this.template({}));
      this.$list = this.$('.scorpion-results');
      return this;
    },

    setActive: function(model) {
      var clauses = [],
          _this = this;
      if (model != null) {
        clauses = model.get('clauses');
      } else if (model == null) {
        if (this.state.locked != null) 
          clauses = this.state.locked.get('clauses');
      }

      clauses = _.map(clauses, function(c) {
        c = _.clone(c);
        c.scorpion = true;
        return c;
      });


      console.log(['setactive', model, this.state.locked, JSON.stringify(clauses)]);
      this.state.where.setSelection(clauses, { silent: true});
      this.trigger('setActive', clauses);
      return this;
    },

    toggleLocked: function(model) {
      if (this.state.locked == model) {
        this.state.locked = null;
      } else {
        this.state.locked = model;
      }
      console.log(['srv.toggleLocked', this.state.locked])
      this.setActive(model);
      return this;
    },

    clickResult: function(view) {
      var model = (view)? view.model : null;
      this.$list.find('.filter-clause').removeClass("locked");
      this.toggleLocked(model); 
      if (view)
        view.$('.filter-clause')
          .toggleClass("locked", this.state.locked == model);
    },

    unlockAll: function(opts) {
      opts || (opts = {});
      if (this.state.locked) {
        console.log(['srv.unlockAll'])
        this.$list.find('.filter-clause').removeClass('locked');
        this.state.locked = null;
        this.trigger('modifiedData', null);
        var selection = this.state.where.get('selection');
        if (opts.clear)
          this.state.where.clearScorpionSelections(opts);
      }
      return this;
    },

    clear: function() {
      console.log(['srv.clear'])
      this.unlockAll();
      this.setActive();
      this.collection.reset();
      return this;
    },

    reset: function() {
      console.log(['srv.reset'])
      this.unlockAll();
      this.setActive();
      this.$list.empty();
      this.collection.each(this.addTo.bind(this));
      return this;
    },


    addTo: function(model) {
      var _this = this;
      var view = new ScorpionResultView({model:model});
      this.$list.append(view.render().el);
      view.on('selected', function() { _this.setActive(view.model); });
      view.on('unselected', function() { _this.setActive(null); });
      view.on('click', this.clickResult.bind(this));
      return this;
    }
  });

  return ScorpionResultsView;
})
