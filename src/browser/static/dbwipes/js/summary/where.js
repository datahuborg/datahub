define(function(require) {
  var Backbone = require('backbone'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      CStat = require('summary/cstat');


  var Where = Backbone.Collection.extend({
    model: CStat,
    url: '/apps/dbwipes/api/schema/',

    initialize: function(attrs) {
      var _this = this;
      this.q = attrs.query;
      this.nbuckets = attrs.nbuckets || 200;
      this.id = Where.id_++;
      this.bTriggerModelSelection = true;
      this.on('add', function(model) {
        this.listenTo(
          model, 
          'change:selection', 
          _this.onModelSelection.bind(_this)
        );
      });
    },

    onModelSelection: function() {
      console.log("onmodelselection " + this.bTriggerModelSelection)
      if (this.bTriggerModelSelection) {
        this.trigger('change:selection');
      }
    },

    // Sets each cstat to the corresponding selection clause
    // @param clauses list of { col:, type:, vals: } objects
    setSelection: function(clauses, opts) {
      this.bTriggerModelSelection = false;

      var col2clause = {};
      _.each(clauses, function(clause) {
        col2clause[clause.col] = clause;
      });

      this.each(function(model) {
        var col = model.get('col');
        model.trigger('setSelection', col2clause[col]);
      });

      console.log(['where.setselection', 'change:selection', clauses]);
      this.trigger('change:selection', opts);

      this.bTriggerModelSelection = true;

    },

    clearScorpionSelections: function(opts) {
      this.bTriggerModelSelection = false;
      this.each(function(model) {
        if (model.get('scorpion')) {
          model.set('selection', [])
          model.trigger('clearScorpionSelection');
        }
      });
      this.trigger('change:selection', opts);
      this.bTriggerModelSelection = true;
    },


    parse: function(resp) {
      var schema = resp.schema;
      var cols = _.keys(schema);
      cols.sort();
      var newstats = _.map(cols, function(col) { 
        var cs = new CStat({
          col: col,
          type: schema[col]
        }); 
        cs.fetch({
          data: {
            username: window.username,
            db: this.q.get('db'),
            table: this.q.get('table'),
            col: col,
            where: _.chain(this.q.get('basewheres'))
              .flatten()
              .pluck('sql')
              .compact()
              .value().join(' AND '),
            nbuckets: this.nbuckets
          }
        });
        return cs;
      }, this)
      return newstats;
    },

    toJSON: function() {
      return _.filter(_.invoke(this.models, 'toJSON'), function(j) {
        return j && j.vals && j.vals.length > 0;
      });
    },

    toSQL: function() {
      var SQL = _.compact(this.map(function(m) {
        return m.toSQLWhere();
      })).join(' and ');
      if (SQL.length)
        return SQL;
      return null;
    }
  });

  Where.id_ = 0;

  return Where;
});
