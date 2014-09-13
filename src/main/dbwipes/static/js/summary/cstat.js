define(function(require) {
  var Backbone = require('backbone'),
      d3 = require('d3'),
      util = require('summary/util');


  require('date');

  var CStat = Backbone.Model.extend({
    url: '/api/column_distribution/',

    defaults: function() {
      return {
        col: null,
        type: null,      // time | timestamp | date | num | str
        stats: [],       // { val:, count:, range:}
        xdomain: [],     // (min, max) or [list of discrete vals]
        ydomain: [],
        selection: [],   // subset of domain
        ready: false,
        scorpion: false  // is the selection based on scorpion predicates
                         // or manually selected?
      }
    },

    initialize: function(attrs) {
      this.set('id', CStat.id_++);
    },


    fetch:  function(options) {
      var _this = this;
      this.trigger('fetch:start');
      this.attributes.ready = false;
      options || (options = { data: {} });
      var complete = options.complete;
      var f = function(resp) {
        _this.trigger('fetch:end');
        if (complete) complete(model, resp, options);
      };
      options.complete = f;
      return Backbone.Model.prototype.fetch.call(this, options);
    },



    parse: function(resp) {
      var data = resp.data;
      var type = data.type,
          stats = data.stats,
          _this = this;

      if (util.isNum(type)) {
        type = data.type = 'num';
      }
      if (util.isStr(type)) {
        type = data.type = 'str';
      }
      if (util.isTime(type)){
        // ensure vals and ranges are date objects
        _.each(stats, function(d) {
          if (type == 'time')  {
            d.val = '2000-01-01T' + d.val;
            d.range = _.map(d.range, function(v) { return '2000-01-01T'+v; });
          }
          d.val = new Date(d.val);
          d.range = _.map(d.range, function(v) {return new Date(v);})
        })
      }
      stats = _.sortBy(stats, 'val');

      var getx = function(d) { return d.val; },
          gety = function(d) { return d.count },
          xdomain = util.getXDomain(stats, type, getx),
          ydomain = [ d3.min(stats, gety), d3.max(stats, gety) ];

      if (ydomain[0] == ydomain[1] || ydomain[0] > 0) 
        ydomain[0] = 0;

      return {
        stats: stats,
        type: type,
        xdomain: xdomain,
        ydomain: ydomain,
        selection: [],
        ready: true
      };
    },



    validate: function(attrs, opts) {
      if (!attrs.col) return "col can't be null";
      if (!attrs.type) return "type can't be null"
    },


    toJSON: function() {
      var type = this.get('type');
      var vals = _.pluck(this.get('selection'), 'range');
      if (vals.length > 0) {
        if (util.isStr(type)) {
          vals = vals.map(function(v) { return _.flatten([v])[0]; });
        } else {
          vals = [d3.min(_.pluck(vals, 0)), d3.max(_.pluck(vals,1))];
          console.log(['cstat.json', vals])
          if (util.isTime(type)) {
            if (type == 'time') 
              vals = vals.map(function(v) { 
                return "'" + v.toLocaleTimeString() + "'";
              });
            else
              vals = vals.map(function(v) { 
                return "'" + v.toISOString() + "'";
              });
          }
        }
      }

      return {
        col: this.get('col'),
        type: this.get('type'),
        vals: vals
      };
    },

    toSQLWhere: function() {
      var sel = this.get('selection');
      if (sel.length == 0) return null;

      var vals = [];
      _.each(sel, function(d) {
        vals = vals.concat(d.range);
      });
      vals = _.uniq(vals);
      var SQL = util.toWhereClause(
        this.get('col'), 
        this.get('type'),
        vals
      );
      if (SQL == '' || SQL == null) return null;
      return SQL;
    }

  });
  CStat.id_ = 0;
  return CStat;
});
