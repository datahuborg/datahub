define(function(require) {
  var Backbone = require('backbone'),
      Handlebars = require('handlebars'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util');


  var DBModel = Backbone.Model.extend({
    url: '/api/databases',
    defaults: function() {
      return {
        dbs: {}   // dbname -> [ tablename,... ]
      };
    }
  });


  var QueryForm = Backbone.View.extend({
    errtemplate: Handlebars.compile($("#q-err-template").html()),
    yexprhtml: "<div><input class='form-control' name='q-y-expr' placeholder='expression'/></div>",
    ycolhtml: "<div><input class='form-control' name='q-y-col' placeholder='attribute'/></div>",

    events: {
      'click .q-add':         "onAggAdd",
      'click .q-submit':      "onSubmit",
      'click .q-where-close': "onWhereClick"
    },

    initialize: function() {
      this.$toggle = $("#q-toggle");
      this.listenTo(this.model, 'change', this.render);
    },

    onAggAdd: function() {
      this.$(".input-ys-expr").append( $(this.yexprhtml));
      this.$(".input-ys-col").append( $(this.ycolhtml));
    },

    onSubmit: function() {
      var db = this.$('input[name=q-db]').val(),
          table = this.$('input[name=q-table]').val(),
          xexpr = this.$('input[name=q-x-expr]').val(),
          xcol = this.$('input[name=q-x-col]').val(),
          xalias = xcol;


      function splitAlias(s, defaultAlias) {
        if (s.indexOf(' as ')) {
          var pair = s.split(' as ');
          return {
            alias: pair[1],
            expr: pair[0]
          };
        }
        return {
          expr: s,
          alias: defaultAlias
        }
      };

      function getVal(idx, el) { return $(el).val(); };

      var x = splitAlias(xexpr, xcol);
      x.col = xcol;
      
      var yexprs = this.$("input[name=q-y-expr]").map(getVal).get();
      var ycols = this.$("input[name=q-y-col]").map(getVal).get();
      var ys = _.zip(yexprs, ycols);
      ys = _.compact(_.map(ys, function(pair) {
        if (pair[0] == '' || pair[1] == '') return null;
        var y = splitAlias(pair[0], pair[1]);
        y.col = pair[1];
        return y;
      }));

      var basewheres = this.$("input[name=q-where]").map(getVal).get();
      basewheres = _.compact(basewheres).map(function(w) {
        return { col: null, type: null, vals: null, sql: w }
      });

      var q = {
        db: db,
        table: table,
        x: x,
        ys: ys,
        basewheres: basewheres,
        where: this.model.get('where'),
        schema: this.model.get('schema')
      };
      this.trigger('submit');
      this.model.set(q);
    },

    

    onWhereClick: function(ev) {
      var el = $(ev.target),
          idx = el.data('idx');
      this.model.get('basewheres').splice(+idx, 1);
      el.parent().remove();
      this.model.trigger('change:basewheres');

    },


    show: function() {
      this.$toggle.text("Hide Query Form");
      this.render().$el.show();
    },

    hide: function() {
      this.$toggle.text("Show Query Form");
      this.render().$el.hide();
    },

    toggle: function() {
      if (this.$el.css('display') == 'none') 
        this.show();
      else
        this.hide();
    },

    render: function(errText) {
      var json = this.model.toJSON(),
          _this = this;
      _.each(json.basewheres, function(clause, idx) {
        clause.idx = idx;
      });
      json['error'] = errText;
      this.$el.attr('id', 'q');
      this.$el.html(this.errtemplate(json));
      return this;
    }
  });
  return QueryForm;
});


