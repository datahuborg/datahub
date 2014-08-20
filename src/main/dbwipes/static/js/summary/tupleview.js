define(function(require) {
  var Backbone = require('backbone'),
      Handlebars = require('handlebars'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util'),
      DrawingView = require('summary/drawingview'),
      QueryForm = require('summary/queryform'),
      Query = require('summary/query');



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



  var TupleQuery = Backbone.Model.extend({
    url: "/api/tuples/",

    defaults: function() {
      return {
        cols: [],
        data: [],
        where: [],
        query: null
      };
    },

    initialize: function() {
      this.prev_json = null;
      this.on('change:where', (function() {
        if (_.isEqual(this.prev_json, this.toJSON())) {
          //console.log(['tupleview.fetch', 'cached']);
          return;
        }
        this.prev_json = _.clone(this.toJSON());
        console.log(['tupleview.fetch', this.toJSON()])
        this.fetch({ 
          data: {
            json: JSON.stringify(this.toJSON()),
            db: this.get('query').get('db')
          }
        });
      }).bind(this));
        
    },


    fetch: function(options) {
      var json = this.toJSON();
      var resp = checkQueryCache(json);
      if (resp) {
        resp = this.parse(resp, options);
        this.set(resp, options);
        if (options.complete) options.complete(this, resp, options);
        if (options.success) options.success(this, resp, options);
        if (options.error) options.error(this, resp, options);

        return;
      }


      options || (options = {});
      var complete = options.complete;
      var f = function(resp) {
        addToCache(json, resp.responseJSON);
        if (complete) complete(model, resp, options);
      };
      options.complete = f;
      return Backbone.Model.prototype.fetch.call(this, options);
    },

    parse: function(resp, opts) {
      var schema = this.get('query').get('schema'),
          q = this.get('query');
      if (resp.data && resp.data.length) {
        resp.cols = _.keys(resp.data[0]);
        var qcols = _.flatten([q.get('x'), q.get('ys')]);
        qcols = _.pluck(qcols, 'col');
        var tcols = _.filter(resp.cols, function(col) {
          return util.isTime(schema[col]) && _.contains(qcols, col);
        });

        _.each(resp.data, function(d) {
          _.each(tcols, function(col) {
            if (schema[col] == 'time') {
              d[col] = '2000-01-01T' + d[col];
            }
            d[col] = new Date(d[col]);
          });
        });
      } else {
        resp.data = [];
      }
      return resp;
    },

    toDataJSON: function() {
      var cols = this.get('cols'),
          data = this.get('data');
      cols.sort();
      data = _.map(data, function(d) {
        return _.map(cols, function(col) { return String(d[col]).substr(0, 10); });
      });

      return {
        nrows: data.length,
        cols: cols,
        data: data
      };
    },

    toJSON: function() {
      var q = this.get('query');
      var json = {
        username: window.username,
        db: this.get('query').get('db'),
        table: this.get('query').get('table'),
        where: this.get('where')
      };
      return json;
    }
  });

  // Query is the model
  var TupleView = Backbone.View.extend({
    template: Handlebars.compile($("#tuple-template").html()),

    initialize: function(attrs) {
      this.w = 500;
      this.h = 300;
      this.lp = 50;
      this.tp = 20;
      this.model = new TupleQuery({query: attrs.query});
      this.listenTo(this.model, 'change:data', this.render);

      this.d3svg = d3.select(this.el)
        .attr('width', this.w+this.lp)
        .attr('height', this.h+this.tp)
      this.g = this.d3svg.append('g')
        .attr('transform', 'translate('+this.lp+', 0)')
      this.d3svg.append('rect')
        .attr('width', this.w+this.lp)
        .attr('height', this.h+this.tp)
        .attr('fill', 'none')

    },

    hide: function() {
      $("#tuples-toggle").text("Show Rows");
      this.$el.hide();
    },
    show: function() {
      $("#tuples-toggle").text("Hide Rows");
      this.$el.show();
    },
    toggle: function() {
      if ($(this.$el).css("display") == 'none') {
        this.show();
      } else {
        this.hide();
      }
    },

    render: function() {
      this.$el.html(this.template(this.model.toDataJSON()));
      return this;
      var q = this.model.get('query'),
          xcol = q.get('x').col,
          xtype = q.get('schema')[xcol],
          data = this.model.get('data');
      if (!data || !data.length) return this;

      var getx = function(d) { return d[xcol]; };
      var xdomain = util.getXDomain(data, xtype, getx);
      var ydomain = [Infinity, -Infinity];
      var ycols = _.uniq(_.map(q.get('ys'), function(ycol) {
        return ycol.col;
      }));
      _.each(ycols, function(y) {
        var yvals = _.filter(_.pluck(data, y), _.isFinite);
        ydomain[0] = Math.min(ydomain[0], d3.min(yvals));
        ydomain[1] = Math.max(ydomain[1], d3.max(yvals));
      }, this);




      var cscales = d3.scale.category10().domain(ycols);
      var xscales = d3.scale.linear().domain(xdomain).range([0, this.w]);
      if (util.isStr(xtype))
        xscales = d3.scale.ordinal().domain(xdomain).rangeRoundBands([0, this.w], .1);
      if (util.isTime(xtype))
        xscales = d3.time.scale().domain(xdomain).range([0, this.w]);
      var yscales = d3.scale.linear().domain(ydomain).range([this.h, this.tp]),
          xf = function(d) {return xscales(d[xcol]); };
      console.log(xscales.domain())

      $(this.g[0]).empty();


      this.g.append('g')
        .attr('class', 'axis x')
        .attr('transform', 'translate(0,' + this.h + ')')
        .call(d3.svg.axis().scale(xscales).orient('bottom'))
      this.g.append('g')  
        .attr('class', 'axis y')
        .call(d3.svg.axis().scale(yscales).orient('left'))

      _.each(ycols, function(y) {
        var yf = function(d) { return yscales(d[y]); };

        this.g.append('g').selectAll('circle')
            .data(data)
          .enter().append('circle')
            .attr({
              class: 'mark',
              cx: xf,
              cy: yf,
              fill: cscales(y),
              r: 2
            });
      }, this);
      console.log(this.el)
      return this;
    }
  });



  return TupleView;

})




