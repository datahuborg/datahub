define(function(require) {
  var _ = require('underscore'),
      d3 = require('d3');
  function isTime(type) {
    return _.contains(['time', 'timestamp', 'date'], type);
  }
  function isNum(type) {
    return _.contains(['integer', 'double precision', 'num', 'int4', 'int', 'int8', 'float8', 'float', 'bigint'], type);
  }
  function isStr(type) {
    return !isTime(type) && !isNum(type);
    return _.contains(['varchar', 'text', 'str'], type);
  }


  function debugMode() {
    try {
      return !$("#fake-type > input[type=checkbox]").get()[0].checked;
    } catch(e) {
      return false;
    }
  }


  function negateClause(SQL) {
    if (!SQL) return null;
    if ($("#selection-type > input[type=checkbox]").get()[0].checked) 
      return SQL;
    return "not(" + SQL + ")";
  }

  // points: [ { yalias:,..., xalias: } ]
  // ycols: [ { col, alias, expr } ]
  function getYDomain(points, ycols) {
    var yaliases = _.pluck(ycols, 'alias'),
        yss = _.map(yaliases, function(yalias) { 
          return _.pluck(points, yalias) 
        }),
        ydomain = [Infinity, -Infinity];

    _.each(yss, function(ys) {
      ys = _.filter(ys, _.isFinite);
      if (ys.length) {
        ydomain[0] = Math.min(ydomain[0], d3.min(ys));
        ydomain[1] = Math.max(ydomain[1], d3.max(ys));
      }
    });
    return ydomain;
  }

  // assume getx(point) and point.range contain x values
  function getXDomain(points, type, getx) {
    var xdomain = null;

    if (isStr(type)) {
      xdomain = {};
      _.each(points, function(d) {
        if (d.range) {
          _.each(d.range, function(o) {
            xdomain[o] = 1;
          });
        }
        xdomain[getx(d)] = 1  ;
      });
      xdomain = _.keys(xdomain);
      return xdomain;
    }


    var diff = 1;
    var xvals = [];
    _.each(points, function(d) {
      if (d.range) xvals.push.apply(xvals, d.range);
      xvals.push(getx(d));
    });
    xvals = _.reject(xvals, _.isNull);

    if (isNum(type)) {
      xvals = _.filter(xvals, _.isFinite);
      xdomain = [ d3.min(xvals), d3.max(xvals) ];

      diff = 1;
      if (xdomain[0] != xdomain[1])
        diff = (xdomain[1] - xdomain[0]) * 0.05;
      xdomain[0] -= diff;
      xdomain[1] += diff;
    } else if (isTime(type)) {
      xvals = _.map(xvals, function(v) { return new Date(v); });
      xdomain = [ d3.min(xvals), d3.max(xvals) ];

      diff = 1000*60*60*24; // 1 day
      if (xdomain[0] != xdomain[1]) 
        diff = (xdomain[1] - xdomain[0]) * 0.05;

      xdomain[0] = new Date(+xdomain[0] - diff);
      xdomain[1] = new Date(+xdomain[1] + diff);
    } 

    //console.log([type, 'diff', diff, 'domain', JSON.stringify(xdomain)]);
    return xdomain;
  }


  function mergeDomain(oldd, newd, type) {
    var defaultd = [Infinity, -Infinity];
    if (isStr(type)) defaultd = [];

    if (oldd == null) 
      return newd;

    if (isStr(type)) 
      return _.union(oldd, newd);

    var ret = _.clone(oldd);
    if (!_.isNull(newd[0]) && (_.isFinite(newd[0]) || isTime(newd[0])))
      ret[0] = d3.min([ret[0], newd[0]]);
    if (!_.isNull(newd[1]) && (_.isFinite(newd[1]) || isTime(newd[1])))
      ret[1] = d3.max([ret[1], newd[1]]);
    return ret;
  }

  function estNumXTicks(xaxis, type, w) {
    var xscales = xaxis.scale();
    var ex = 40.0/5;
    var xticks = 10;
    while(xticks > 1) {
      if (isStr(type)) {
        var nchars = d3.sum(_.times(
          Math.min(xticks, xscales.domain().length),
          function(idx){return (""+xscales.domain()[idx]).length+.8})
        )
      } else {
        var fmt = xscales.tickFormat();
        var fmtlen = function(s) {return fmt(s).length+.8;};
        var nchars = d3.sum(xscales.ticks(xticks), fmtlen);
      }
      if (ex*nchars < w) break;
      xticks--;
    }
    xticks = Math.max(1, +xticks.toFixed());
    return xticks;
  }

  function setAxisLabels(axis, type, nticks) {
    var scales = axis.scale();

    axis.ticks(nticks).tickSize(0,0);

    if (isStr(type)) {
      var skip = scales.domain().length / nticks;
      var idx = 0;
      var previdx = null;
      var tickvals = [];
      while (idx < scales.domain().length) {
        if (previdx == null || Math.floor(idx) > previdx) {
          tickvals.push(scales.domain()[Math.floor(idx)])
        }
        idx += skip;
      }
      axis.tickValues(tickvals);
    } 
    return axis;

  }


  function toWhereClause(col, type, vals) {
    if (!vals || vals.length == 0) return null;
    var SQL = null;
    var re = new RegExp("'", "gi");
    if (isStr(type)) {
        SQL = [];
        if (_.contains(vals, null)) {
          SQL.push(col + " is null");
        }

        var nonnulls = _.reject(vals, _.isNull);
        if (nonnulls.length == 1) {
          var v = nonnulls[0];
          if (_.isString(v)) 
            v = "'" + v.replace(re, "\\'") + "'";
          SQL.push(col + " = " + v);
        } else if (nonnulls.length > 1) {
          vals = _.map(nonnulls, function(v) {
            if (_.isString(v)) 
              return "'" + v.replace(re, "\\'") + "'";
            return v;
          });
          SQL.push(col + " in ("+vals.join(', ')+")");
        }

        if (SQL.length == 0)
          SQL = null;
        else if (SQL.length == 1)
          SQL = SQL[0];
        else
          SQL = "("+SQL.join(' or ')+")";
    } else {
      if (isTime(type)) {
        if (type == 'time') {
          var val2s = function(v) { 
            // the values could have already been string encoded.  
            if (_.isDate(v))
              return "'" + (new Date(v)).toLocaleTimeString() + "'";
            return v;
          };
        } else {
          var val2s = function(v) { 
            if(_.isDate(v)) 
              return "'" + (new Date(v)).toISOString() + "'"; 
            return v;
          };
        }
        //vals = _.map(vals, function(v) { return new Date(v)});
      } else {
        var val2s = function(v) { return +v };
      }
      if (vals.length == 1) {
        SQL = col + " = " + val2s(vals[0]);
      } else {
        SQL = [
          val2s(d3.min(vals)) + " <= " + col,
          col + " <= " + val2s(d3.max(vals))
        ].join(' and ');
      }
    }
    return SQL;

  }


  return {
    isTime: isTime,
    isNum: isNum,
    isStr: isStr,
    estNumXTicks: estNumXTicks,
    setAxisLabels: setAxisLabels,
    toWhereClause: toWhereClause,
    negateClause: negateClause,
    getXDomain: getXDomain,
    getYDomain: getYDomain,
    mergeDomain: mergeDomain,
    debugMode: debugMode
  }
})


