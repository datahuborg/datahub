define(function(require) {
  var Backbone = require('backbone'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util');

  window.queryCache = queryCache = {};
  function checkQueryCache(json) {
    var key = JSON.stringify(json);
    return queryCache[key];
  }

  function addToCache(json, data) {
    var key = JSON.stringify(json);
    var n = _.size(queryCache);
    if (!_.contains(queryCache, key) && n > 10) {
      _.each(_.last(_.keys(queryCache), n - 10), function(k) {
        delete queryCache[k];
      });
    }
    queryCache[key] = data;
    return;
  }

  var Query = Backbone.Model.extend({
    url: '/api/query',

    defaults: function() {
      return {
        x: null,            // { col:, expr:}
        ys: null,
        schema: null,       // { col -> type }
        where: [],          // this changes depending on how user inteacts with rules/selection
        basewheres: [],     // this WHERE is part of the query and should not be modified
                            // only way to set basewhere is to click on a rule
        table: null,
        db: null,
        data: null,
        limit: null,
      }
    },


    initialize: function() {
      this.on('change:x change:ys change:basewheres', this.onChange);
      this.on('change:db change:table', this.onChangeDB);
    },

    ensureX: function() {
      var x = this.get('x');
      x = (_.isString(x))? {col:x, expr:x} : x;
      if (!x.alias) x.alias = x.col;
      this.attributes['x'] = x;
    },

    ensureYs: function() {
      var ys = this.get('ys');
      ys = (_.isArray(ys))? ys: [ys];
      ys = _.map(ys, function(y) {
        y = (_.isString(y))? {col:y, expr: y} : y;
        if (!y.alias) y.alias = y.col;
        return y;
      })
      this.attributes['ys'] = ys;
    },


    onChangeDB: function() {
      this.set('where', []);
      this.set('basewheres', []);
      this.onChange()
    },

    onChange: function() {
      this.ensureX();
      this.ensureYs();
      console.log("fetching new query " + this.get('where'))
      this.fetch({
        data: {
          json: JSON.stringify(this.toJSON()),
          db: this.get('db')
        }
      });
    },

    fetch: function(options) {
      var json = this.toJSON();
      var resp = checkQueryCache(json);
      if (resp) {
        console.log(['q.fetch', 'cache hit', json, resp])
        resp = this.parse(resp, options);
        this.set(resp, options);

        if (options.complete) options.complete(this, resp, options);
        if (options.success) options.success(this, resp, options);
        if (options.error) options.error(this, resp, options);

        return;
      }

      $("#q_loading").show();
      var model = this;
      options || (options = {});
      options.data || (options.data = this.toJSON());
      var complete = options.complete;
      var f = function(resp) {
        $("#q_loading").hide();
        addToCache(json, resp.responseJSON);
        if (complete) complete(model, resp, options);
      };
      options.complete = f;
      
      return Backbone.Model.prototype.fetch.call(this, options);
    },


    // parse /api/query/ results
    parse: function(resp, opts) {
      var xcol = this.get('x'),
          schema = resp.schema || this.get('schema');

      if (resp.data) {
        var type = schema[xcol.col];

        if (util.isTime(type)) {
          if (type == 'time') {
            _.each(resp.data, function(d) {
              d[xcol.alias] = "2000-01-01T" + d[xcol.alias];
            });
          }
          _.each(resp.data, function(d) {
            d[xcol.alias] = new Date(d[xcol.alias]);
          });

          resp.data = _.reject(resp.data, function(d) {
            var vals = _.values(d);
            return _.any(_.map(vals, _.isNull));
          });
        }
      }
      return resp;

    },



    validate: function() {
      var errs = [];
      if (!this.get('db')) 
        errs.push("need database");
      if (!this.get('table')) 
        errs.push("need table name");
      if (!this.get('x')) 
        errs.push("need grouping attribute (x)");
      if (!this.get('ys')) 
        errs.push("need aggregations (y)");
      if (!this.get('data'))
        errs.push("need data!");
      if (errs.length) 
        return errs.join('\n');
    },


    toJSON: function() {
      var basewheres = this.get('basewheres') || [];
      basewheres = _.compact(_.flatten(basewheres));
      var where = this.get('where');

      var ret = {
        x: this.get('x'),
        ys: this.get('ys'),
        table: this.get('table'),
        db: this.get('db'),
        where: where,
        basewheres: basewheres,
        limit: this.get('limit'),
        negate: !$("#selection-type > input[type=checkbox]").get()[0].checked
        //query: this.toSQL()
      };
      
      return ret;
    },

    toSQL: function() {
      throw Error("Query.toSQL should not be called anymore");
    }

  })

  return Query;
});
