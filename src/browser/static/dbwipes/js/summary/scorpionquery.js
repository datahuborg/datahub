define(function(require) {
  var Backbone = require('backbone'),
      $ = require('jquery'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util'),
      ScorpionResult = require('summary/scorpionresult'),
      ScorpionResults = require('summary/scorpionresults')


  var ScorpionQuery = Backbone.Model.extend({
    url: '/apps/dbwipes/api/scorpion/',

    defaults: function() {
      return {
        badselection: {},   // y -> []
        goodselection: {},
        selection: {},
        errtypes: {},
        erreqs: {},
        ignore_cols: [],
        query: null,
        drawing: null,
        results: new ScorpionResults(),
        _results: [],
        top_k_results: {}  // c_val -> list of rules
      }
    },


    initialize: function() {
    },

    merge: function(key, selection) {
      //
      // TODO: remove from other selection values in new selection
      //
      if (selection == null || _.size(selection) == 0) return;
      var curSel = this.get(key) || {};
      _.each(selection, function(ds, yalias) {
        if (!curSel[yalias]) 
          curSel[yalias] = [];
        curSel[yalias] = _.union(curSel[yalias], ds);
      }, this)
      this.set(key, curSel);
      this.trigger('change')
    },

    // number of selections for {key}selection
    count: function(key) {
      return d3.sum(
        _.values(this.get(key))
          .map(function(ds) { return ds.length; })
      );
    },

    // mean of y vals for {key}selection
    mean: function(key, yalias) {
      var selected = this.get(key)[yalias];
      if (!selected) return null;

      return d3.mean(selected.map(function(d) {
        return d[yalias];
      }));
    },

    validate: function() {
      var errs = [],
          yaliases = _.keys(this.get('badselection')),
          drawing = this.get('drawing');

      this.set('errtypes', {});


      // verify errtype is eq if a line is drawn
      if (drawing && drawing.get('path') && drawing.get('path').length) {
        _.each(yaliases, function(yalias) {
          var ds = this.get('badselection')[yalias];
          ds.sort(function(a,b) { return a.px - b.px; });

          var ys = drawing.interpolate(_.pluck(ds, 'px'));

          if (ys == null) {
            errs.push("<div>drawn path doesn't cover selected points</div>");
          } else {
            ys = _.map(ys, drawing.inverty.bind(drawing));
            this.get('errtypes')[yalias] = 1;
            this.get('erreqs')[yalias] = ys;
          }

        }, this);
      } else {
        _.each(yaliases, function(yalias) {
          var badmean = this.mean('badselection', yalias),
              goodmean = this.mean('goodselection', yalias);
          if (!badmean) return;
          if (badmean && goodmean == null) 
            this.get('errtypes')[yalias] = 2;
            //errs.push("<div>select good examples for <strong>"+yalias+"</strong></div>");
          else
            this.get('errtypes')[yalias] = (goodmean > badmean)? 3 : 2;
        }, this) 
      }


      if (errs.length) 
        return errs.join('\n');
    },

    parse: function(resp) {
      //
      // results: [ { score:, c_range:, clauses:, alt_clauses:, } ]
      // top_k_results: { 
      //  yalias: { 
      //    c_val: [ { score:, c_range:, clauses: } ] 
      //   } 
      // }
      //
      console.log("scorpionquery got response");
      console.log(resp);
      if (resp.results) {
        var q = this.get('query'),
            results = this.get('results');

        var newresults = _.map(resp.results, function(r) {
          r.query = q;
          return new ScorpionResult(r);
        });

        results.reset(newresults);
        resp._results = newresults;
        resp.results = results;
      }
      if (resp.top_k_results) {
        var top_k = {};
        _.each(resp.top_k_results, function(r) {
          var c = r.c;
          if (!top_k[c]) top_k[c] = [];
          r.query = q;
          r = new ScorpionResult(r);
          top_k[c].push(r);
        });
        resp.top_k_results = top_k;
      }
      console.log("scorpionquery parsed true response")
      return resp;
    },


    toJSON: function() {
      var json = {
        schema: this.get('query').get('schema'),
        nselected: this.count('selection'),
        nbad: this.count('badselection'),
        ngood: this.count('goodselection'),
        badselection: this.get('badselection'),
        goodselection: this.get('goodselection'),
        ignore_cols: this.get('ignore_cols'),
        errtypes: this.get('errtypes'),
        erreqs: this.get('erreqs'),
        query: this.get('query').toJSON()
      };
      return json;
    },

    toSQL: function() {
      return "";
    }

  })

  return ScorpionQuery;
});
