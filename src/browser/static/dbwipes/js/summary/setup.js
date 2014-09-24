define(function(require) {
  var Backbone = require('backbone'),
      $ = require('bootstrap'),
      d3 = require('d3'),
      _ = require('underscore'),
      Where = require('summary/where'),
      util = require('summary/util'),
      ScorpionQuery = require('summary/scorpionquery'),
      ScorpionQueryView = require('summary/scorpionview'),
      ScorpionResult = require('summary/scorpionresult'),
      ScorpionResults = require('summary/scorpionresults'),
      ScorpionResultsView = require('summary/scorpionresultsview'),
      TupleView = require('summary/tupleview'),
      DrawingView = require('summary/drawingview'),
      Where = require('summary/where'),
      WhereView = require('summary/whereview'),
      CStat = require('summary/cstat'),
      CStatView = require('summary/cstatview'),
      CStatsView = require('summary/cstatsview'),
      Query = require('summary/query'),
      QueryForm = require('summary/queryform'),
      QueryView = require('summary/queryview'),
      QueryWhereView = require('summary/querywhereview'),
      util = require('summary/util');

  var setupButtons = function(q, qv) {
    $("[data-toggle=tooltip]").tooltip();

    var st_on_text = "Visualization shows what data matching your filter" ,
        st_off_text = "Visualization removes data matching your filter";
    $("#selection-type > input[type=checkbox]").click(function() {
      where.trigger("change:selection");
      var txt = (this.checked)? st_on_text : st_off_text;
      $("#selection-type")
        .attr('title', txt)
        .tooltip('fixTitle')
        .tooltip('show');
    });
    $("#selection-type")
      .attr('title', st_on_text)
      .tooltip('fixTitle');


    $("#apply-btn").click(function() {
      if (qv.overlayquery && qv.overlayquery.get('where')) {
        var ws = _.chain(qv.overlayquery.get('where'))
          .filter(function(w) { return w.vals && w.vals.length; })
          .compact()
          .uniq()
          .map(function(w) { return util.toWhereClause(w.col, w.type, w.vals);})
          .map(function(w) { return util.negateClause(w); })
          .map(function(w) { return {col: null, sql: w}; })
          .value();
        var bws = q.get('basewheres');
        bws.push.apply(bws, ws);
        bws = _.uniq(bws, function(bw) { return bw.sql; });
        q.set('basewheres', bws);
        q.trigger('change:basewheres');
        window.where.trigger('change:selection');
      }
    });

  };


  var setupBasic = function() {
    var q = new Query();
    var qv = new QueryView({ model: q })
    $("#right").prepend(qv.render().$el);


    var where = new Where({
      query: q,
      nbuckets: 200
    });
    var whereview = new WhereView({
      collection: where, 
      el: $("#temp-where")
    });
    var csv = new CStatsView({
      collection: where, 
      el: $("#facets")
    });
    var qwv = new QueryWhereView({
      model: q,
      el: $("#perm-where")
    });
    var qf = new QueryForm({model: q, el: $("#query-form-container")});
    q.on('change:db change:table change:basewheres', function() {
      var whereSQL = _.chain(q.get('basewheres'))
        .flatten()
        .pluck('sql')
        .compact()
        .value()
        .join(' AND ');

      where.fetch({
        data: {
          username: window.username,
          db: q.get('db'),
          table: q.get('table'),
          where: whereSQL
        },
        reset: true
      });

      qf.render();
    });
    qf.on("submit", function() {
      qv.resetState();
    });
    $("#q-toggle").click(qf.toggle.bind(qf));


    // connect drag and drop from cstatsview to query form
    (function() {
      function checkHit(activeEl, targetId, ev) {
        // check if overlaps with qf elements
        var xel = $(targetId);
        var parPos = xel.offsetParent().position();
        var xPos = xel.position();
        xPos.left += parPos.left;
        xPos.top += parPos.top;
        var xDim = xel.get()[0].getBBox();
        var pad = 3;
        var cstatOff = {
          left: initOffset.left + ev.pageX - initMouse.left,
          top: initOffset.top + ev.pageY - initMouse.top
        };

        return !(
          xPos.left+xDim.width < cstatOff.left-pad ||
          cstatOff.left+activeEl.width()+pad+pad < xPos.left ||
          xPos.top+xDim.height < cstatOff.top-pad ||
          cstatOff.top+activeEl.height()+pad+pad < xPos.top
        ) 
      }


      var activeCStat = null;
      var activeEl = null;
      var initOffset = null;
      var initMouse = null;
      var parent = null;
      csv.on("dragStart", function(cstatview, ev) {
        activeCStat = cstatview.model;
        activeEl = cstatview.$el.find(".col-name");
        parent = activeEl.parent();
        initOffset = activeEl.offset();
        initMouse = {left: ev.pageX, top: ev.pageY}
        activeEl = activeEl.clone();
        activeEl.remove().appendTo($("body"));
      });
      csv.on("drag", function(cstatview, ev) {
        if (activeEl) {
          activeEl.css({
            position: "absolute",
            left: initOffset.left + ev.pageX - initMouse.left,
            top: initOffset.top + ev.pageY - initMouse.top
          });
          if (checkHit(activeEl, "#viz .xaxis", ev)) {
            d3.select("#viz .xaxis").classed("dropactive", true);
            activeEl.addClass("active");
          } else {
            d3.select("#viz .xaxis").classed("dropactive", false);
            activeEl.removeClass("active");

            if (util.isNum(cstatview.model.get("type"))) {
              if (checkHit(activeEl, "#viz .yaxis", ev)) {
                d3.select("#viz .yaxis").classed("dropactive", true);
                activeEl.addClass("active");
              } else {
                d3.select("#viz .yaxis").classed("dropactive", false);
                activeEl.removeClass("active");
              }
            }
          }

        }
      });
      csv.on("dragEnd", function(cstatview, ev) {
        if (activeEl) {
          if (checkHit(activeEl, "#viz .xaxis", ev)) {
            qf.$("input[name=q-x-expr]").val(cstatview.model.get("col"));
            qf.$("input[name=q-x-col]").val(cstatview.model.get("col"));
            qf.onSubmit();
          } else if (checkHit(activeEl, "#viz .yaxis", ev)) {
            qf.$("input[name=q-y-expr]").remove();
            qf.$("input[name=q-y-col]").remove();
            qf.onAggAdd.call(qf);
            if (util.isNum(cstatview.model.get("type"))) {
              qf.$("input[name=q-y-expr]").val("avg("+cstatview.model.get("col")+")");
              qf.$("input[name=q-y-col]").val(cstatview.model.get("col"));
              qf.onSubmit();
            }
          } 
          d3.select("#viz .xaxis").classed("dropactive", false);
          d3.select("#viz .yaxis").classed("dropactive", false);
          activeEl.remove();
          activeCStat = activeEl = null;
        }
      });
    })();


    where.on('change:selection', function() {
      var defaultOpts = {silent: false, clear: true};
      var opts = null;
      arguments.length && (opts = _.last(arguments))
      opts || (opts = {silent: false});
      opts = _.extend(defaultOpts, opts);
      console.log(['summary.js', 'where.onselection', opts]);
      if (!opts.silent) {
        if (window.srv) {
          window.srv.unlockAll({clear: false});
          window.psrv.unlockAll({clear: false});
        }
        qv.renderWhereOverlay(where.toJSON());
      }
    });
    window.q = q;
    window.qv = qv;
    window.qf = qf;
    window.qwv = qwv;
    window.where = where;
    window.csv = csv;
  }


  var setupScorpion = function(enableScorpion, q, qv, where) {
    if (!enableScorpion) {
      $("#facet-togglecheckall").css("opacity", 0);
      return;
    }

    var srs = null,
        srv = null,
        sq = null,
        sqv = null,
        psrs = null,
        psrv = null;

    srs = new ScorpionResults()
    srv = new ScorpionResultsView({
      collection: srs, 
      where: where, 
      query: q
    });
    psrs = new ScorpionResults()
    psrv = new ScorpionResultsView({
      collection: psrs, 
      where: where, 
      query: q
    });
    $("#scorpion-results-container").append(srv.render().el);
    $("#scorpion-partialresults-container").append(psrv.render().el);
    

    sq = new ScorpionQuery({
      query: q, 
      results: srs, 
      partialresults: psrs
    });
    sqv = new ScorpionQueryView({
      model: sq, 
      queryview: qv
    });
    $("body").append(sqv.render().$el.hide());


    var scr_btn = $(".walkthrough-btn");
    scr_btn.click(function() {
      sqv.$el.toggle()
    });

    srv.on('setActive', function(whereJson) {
      console.log(['summary.js', 'setactive', whereJson])
      qv.renderWhereOverlay(whereJson);
    });
    psrv.on('setActive', function(whereJson) {
      qv.renderWhereOverlay(whereJson);
    });


    q.on('change:db change:table', function() {
      sq.set('badselection', {});
      sq.set('goodselection', {});
    });
    qv.on('resetState', function() {
      sq.set('badselection', {});
      sq.set('goodselection', {});
      sq.set('selection', {});
    });
    qv.on('change:selection', function(selection) {
      sq.set('selection', selection);
    });
    qv.on('change:drawing', function(drawingmodel) {
      sq.set('drawing', drawingmodel);
    });


    window.sq = sq;
    window.sqv = sqv;
    window.srs = srs;
    window.srv = srv;
    window.psrs = psrs;
    window.psrv = psrv;
  };


  var setupTuples = function(q, srv, where) {
    var tv = new TupleView({
      query: q, 
      el: $("#tuples").get()[0]
    });
    tv.hide();

    if (srv) {
      srv.on('setActive', function(whereJSON) {
        tv.model.set('where', whereJSON);
      });
    }
    where.on('change:selection', function() {
      tv.model.set('where', where.toJSON());
      tv.model.trigger('change:where')
    });
    q.on('change', function() {
      var wheres = _.union(q.get('basewheres'), q.get('where'));
      wheres = _.chain(wheres).flatten().compact().value();
      tv.model.set('where', wheres);
      tv.model.trigger('change:where');
    });

    $("#tuples-toggle").click(tv.toggle.bind(tv));
    window.tv = tv;
  };


  return {
    setupBasic: setupBasic,
    setupButtons: setupButtons,
    setupScorpion: setupScorpion,
    setupTuples: setupTuples
  };
});

