define(function(require) {
  var Backbone = require('backbone'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util');

  var ScorpionResult = Backbone.Model.extend({
    defaults: function() {
      return {
        query: null,        // Query object
        partial: false,     // is this a result while scoprion runs
                            // or the final result
        yalias: null,
        score: 0,
        count: 0,
        c_range: [],     // [minc, maxc]
        clauses: [],     // { col:, type:, vals: }
        alt_rules: [],   // [ {col:, type:, vals:} ]
        id: ScorpionResult._id++
      }
    },

    initialize: function() {
    },


    // return as a format consistent with
    // how Where.toJSON() generates toJSON() objects
    // [{
    //    col: 
    //    type:
    //    vals:
    // }]
    toSQLJSON: function() {
      return this.get('clauses');
    },


    toJSON: function() {
      var json = {
        score: this.get('score'),
        partial: this.get('partial'),
        clauses: _.map(this.get('clauses'), function(c){
          var vals = c.vals;
          if (util.isNum(c.type))
            vals = _.map(c.vals, function(v) {return +v.toPrecision(3); });
          return util.toWhereClause(c.col, c.type, vals);//.substr(0, 20);
        }),
        alt_rules: _.map(this.get('alt_rules'), function(r) {
          return _.map(r, function(c) {
            var vals = c.vals;
            if (util.isNum(c.type))
              vals = _.map(c.vals, function(v) {return +v.toPrecision(3); });
            return util.toWhereClause(c.col, c.type, vals);//.substr(0, 20);
          });
        }),
        c_range: this.get('c_range').join(' - '),
        yalias: this.get('yalias')
      };
      //console.log(json)
      return json;
    },

    toSQL: function() {
      var SQL = _.map(this.get('clauses'), function(clause) {
        return util.toWhereClause(clause.col, clause.type, clause.vals); 
      }).join(' and ');
      if (SQL.length > 0)
        return SQL;
      return null;
    }
  });
  ScorpionResult._id = 0;


  return ScorpionResult;
});
