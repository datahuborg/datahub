// CSTatView
define(function(require) {
  var Handlebars = require('handlebars'),
      Backbone = require('backbone'),
      d3 = require('d3'),
      $ = require('jquery'),
      util = require('summary/util');


  return Backbone.View.extend({

    template: Handlebars.compile($("#cstat-template").html()),

    initialize: function() {
      this.state = {
        xscales: null,
        yscales: null,
        xaxis: null,
        yaxis: null,
        series: null,
        w: 350,
        h: 50,
        lp: 70,
        bp: 18,
        rectwidth: 1,
        marktype: 'rect'
      }
      this.listenTo(this.model, 'setSelection', this.setSelection);
      this.listenTo(this.model, 'clearScorpionSelection', this.clearScorpionSelection);
      this.listenTo(this.model, 'change:selection', this.setCount)
      this.listenTo(this.model, 'change:stats', this.render)
      //this.listenTo(this.model, 'fetch:start', this.showLoading);
      //this.listenTo(this.model, 'fetch:stop', this.hideLoading);
    },

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      if (!window.enableScorpion) this.$('.errcol').hide();
      if (this.model.get('ready')) {
        this.$('.cstat-loading').hide();
        this.renderPlot(this.$('svg.cstat-plot-svg'));
      } else {
        this.$('.cstat-loading').show();
        this.$('svg.cstat-plot-svg').hide();
      }
      this.setupDragAndDrop();
      return this;
    },

    showLoading: function() {
      this.$("svg.cstat-plot-svg").hide();
      this.$('.cstat-loading').show();
      return this;
    },

    hideLoading: function() {
      this.$("svg.cstat-plot-svg").show();
      this.$('.cstat-loading').hide();
      return this;
    },

    setupDragAndDrop: function() {
      var _this = this;
      var el = this.$el.find(".col-name");
      el.on("mousedown", function(ev) {
        _this.trigger("dragStart", _this, ev);
        $("body")
          .on("mousemove.cstat", function(ev) {
            _this.trigger("drag", _this, ev);
          })
          .on("mouseup.cstat", function(ev) {
            _this.trigger("dragEnd", _this, ev);
            $("body")
              .off("mousemove.cstat")
              .off("mouseup.cstat")
          })

      });

    },

    setupScales: function() {
      var xdomain = this.model.get('xdomain'),
          ydomain = this.model.get('ydomain'),
          type = this.model.get('type');
      this.state.xscales = this.makeScales('x', xdomain, [0, this.state.w], type);
      this.state.yscales = this.makeScales('y', ydomain, [this.state.h, 5], 'num');


      // create axes
      this.state.xaxis = d3.svg.axis()
        .scale(this.state.xscales)
        .orient('bottom');
      this.state.yaxis = d3.svg.axis()
        .scale(this.state.yscales)
        .orient('left');

      var nticks = util.estNumXTicks(
          this.state.xaxis, 
          this.model.get('type'), 
          this.state.w
      );
      util.setAxisLabels(this.state.xaxis, this.model.get('type'), nticks);
      this.state.yaxis.ticks(2).tickSize(0,0);
    },

    makeScales: function(scaletype, domain, range, type) {
      var scales = d3.scale.linear();
      if (util.isTime(type)) 
        scales = d3.time.scale();
      else if (util.isStr(type)) 
        scales = d3.scale.ordinal();
      
      if (scaletype == 'y' && util.isNum(type)) {
        if (false && domain[1] > d3.max([1,domain[0]]) * 1000)  {
          scales = d3.scale.log()
          domain[0] = d3.max([domain[0], 1]);
        }
      }

      scales.domain(domain).range(range);
      if (util.isStr(type)) {
        scales.rangeRoundBands(range, 0.1);
        if (scales.rangeBand() <= 2) {
          scales.rangePoints(range);
        }
      }
      return scales;
    },


    renderAxes: function(el) {
      var xel = el.append('g')
        .attr('class', 'axis x xaxis')
        .attr('transform', "translate(0,"+this.state.h+")")
      xel.append('rect')
        .attr('width', this.state.w)
        .attr('height', this.state.bp)
        .attr('fill', 'none')
        .attr('stroke', 'none')
        .style('pointer-events', 'all');
      xel.call(this.state.xaxis)

      var yel = el.append('g')
        .attr('class', 'axis y yaxis');
      yel.append('rect') 
        .attr('width', this.state.lp)
        .attr('height', this.state.h)
        .attr('x', -this.state.lp)
        .attr('fill', 'none')
        .attr('stroke', 'none')
        .style('pointer-events', 'all');
      yel.call(this.state.yaxis)
    },


    renderData: function(el) {
      var col = this.model.get('col'),
          type = this.model.get('type'),
          stats = this.model.get('stats'),
          xscales = this.state.xscales,
          yscales = this.state.yscales,
          h = this.state.h

      if (util.isStr(type)) {
        this.state.rectwidth = width = xscales.rangeBand();
        el.selectAll('rect')
            .data(stats)
          .enter().append('rect')
            .attr({
              class: 'mark',
              width: d3.max([1,xscales.rangeBand()]),
              x: function(d) { return xscales(d.val) },
              height: function(d) {return Math.max(2, yscales(0)-yscales(d.count));},
              y: function(d) { return Math.min(h-2, yscales(d.count));}
            })
      } else {
        var xs =_.pluck(stats, 'val');

        //if (xs.length == 0) return;

        xs = _.uniq(_.map(xs, xscales));
        xs.push.apply(xs, xscales.range());
        xs.sort();
        var intervals = _.times(xs.length-1, function(idx) { return xs[idx+1] - xs[idx]});
        var width = null;
        if (intervals.length)
          width = d3.min(intervals) - 0.5
        if (!width)
          width = 10;
        this.state.rectwidth = width = d3.max([1, width])

        var minv = xscales.invert(d3.min(xs) - d3.max([5, width])),
            maxv = xscales.invert(d3.max(xs) + d3.max([5, width]));
        xscales.domain([minv, maxv]);

        if (!_.isNaN(xscales.domain()[0]) && col == 'light'){
          var args = [this.model.get('col'), type,  stats.length, stats[0]];
          args.push('xscale')
          args.push.apply(args, xscales.domain());
          args.push('->')
          args.push.apply(args, xscales.range());
          args.push('yscale')
          args.push.apply(args, yscales.domain());
          args.push('->')
          args.push.apply(args, yscales.range());
          console.log(args);
        }


        el.selectAll('rect')
            .data(stats)
          .enter().append('rect')
            .attr({
              class: 'mark',
              width: function(d) { return d3.max([width, xscales(d.range[1]) - xscales(d.range[0])]) },
              height: function(d) {return Math.max(2, h-yscales(d.count))},
              x: function(d) {return xscales(d.range[0]);},
              y: function(d) { return Math.min(h-2, yscales(d.count)); }
            })
      } 


    },

    setCount: function() {
      var count = this.model.get('selection').length;
      var sum = d3.sum(_.map(this.model.get('selection'), function(d) {
        return d.count;
      }));
      if (count)
        this.$('.count').text(count + ' vals ('+sum+' rows)');
      else
        this.$('.count').text(null);
    },

    // programatically set the selection
    // the expectation is that the model.set calls in the method
    // will not trigger "change" events
    setSelection: function(clause) {
      function withinClause(clause, val) {
        if (clause == null) return false;
        if (util.isStr(clause.type)) {
          return _.contains(clause.vals, val);
        } else {
          return clause.vals[0] <= val && val <= clause.vals[1];
        }
      };

      if (this.d3brush) {
        this.d3brush.extent([]);
        this.d3brush.clear();
      }


      if (clause) {
        if (!util.isStr(clause.type)) {
          var extent = [
            d3.max([clause.vals[0], this.state.xscales.domain()[0]]),
            d3.min([clause.vals[1], this.state.xscales.domain()[1]])
          ];
          this.d3brush.extent(extent);
        }
      }
      if (this.d3gbrush && this.d3brush)
        this.d3brush(this.d3gbrush);

      var selected = [];
      if (clause) {
        this.d3svg.selectAll('.mark')
          .classed('selected', false)
          .classed('highlighted', function(d) {
            if (withinClause(clause, d.val)) {
              selected.push(d);
              return true;
            } 
            return false;
          })
          .classed('faded', function(d) {
            return !withinClause(clause, d.val);
          })
      } else {
        this.d3svg.selectAll('.mark')
          .classed('selected', false)
          .classed('highlighted', false)
          .classed('faded', false)
      }

      if (clause) 
        this.model.set('scorpion', true);
      else
        this.model.set('scorpion', false);
      this.model.set('selection', selected, {silent: true});

    },

    clearScorpionSelection: function() {
      this.d3brush.clear();
      this.d3brush(this.d3gbrush);
      this.d3svg.selectAll('.mark')
        .classed('selected', false)
        .classed('highlighted', false)
        .classed('faded', false);
    },


    renderBrushes: function(el) {
      var xscales = this.state.xscales,
          h = this.state.h,
          type = this.model.get('type'),
          _this = this;

      var within = function(d, e) {
        if (e[0] == e[1]) return false;
        if (type == 'str') {
          var bmin = xscales(d.val) + xscales.rangeBand()/4,
              bmax = xscales(d.val) + 3*xscales.rangeBand()/4;
          var b = !(e[1] < bmin || bmax < e[0]);
        } else {
          var width = xscales(d.range[1]) - xscales(d.range[0]),
              bmin = xscales(d.val)+width/4.0,
              bmax = xscales(d.val)+3.0*width/4.0;
          var b = !(xscales(e[1]) < bmin || bmax < xscales(e[0]));
        }
        return b;
      };

      var brushf = function(p) {
        var e = brush.extent()
        var selected = [];
        el.selectAll('.mark')
          .classed('highlighted', false)
          .classed('faded', false)
          .classed('selected', function(d){ return within(d, e); })
          .each(function(d) { if (within(d, e)) selected.push(d); })
        if (d3.event.type == 'brushend') {
          _this.model.set('scorpion', false);
          _this.model.set('selection', selected);
        }
      }

      var brush = d3.svg.brush()
          .x(xscales)
          .on('brush', brushf)
          .on('brushend', brushf)
          .on('brushstart', brushf);
      var gbrush = el.append('g')
          .attr('class', 'brush')
          .call(brush);
      gbrush.selectAll('rect')
          .attr('height', h)

      this.d3brush = brush;
      this.d3gbrush = gbrush;

    },

    renderZoom: function(el) {
      var _this = this,
          xscales = this.state.xscales,
          xaxis = this.state.xaxis,
          width = this.state.rectwidth,
          yaxis = this.state.yaxis,
          yscales = this.state.yscales,
          h = this.state.h;


      var yzoomf = function(el) {
        var yaxis = this.state.yaxis;
        var yscales = this.state.yscales;
        el.select('.axis.y').call(yaxis);
        el.selectAll('.mark')
          .attr('y', function(d) {
            return Math.max(0, Math.min(h, yscales(d.count)-2));
          })
          .attr('height', function(d) {
            var bot = Math.max(0, Math.min(h, yscales(d.count)-2));
            var height = yscales(0) - bot;
            return Math.min(h-bot, Math.max(2, height));
          })
      };
      yzoomf = _.bind(yzoomf, this, el);


      var yshiftf = function(el, yzoomf) {
        var yzoom = this.yzoom;
        var yStart = d3.event.y;
        var curYScale = yzoom.scale();
        var yscales = this.state.yscales;

        if (d3.event.shiftKey) {
          d3.select('body')
            .on('mousemove.cstaty', function() {
              var diff = ((yStart - d3.event.y) / 10);
              if (diff >= 0) { 
                diff += 1.0; 
              } else {
                diff = 1.0 / (Math.abs(diff)+1);
              }
              yzoom.scale(diff*curYScale);
            })
            .on('mouseup.cstaty', function() {
              d3.select('body')
                .on('mousemove.cstaty', null)
                .on('mouseup.cstaty', null);
            });
        }
      }
      yshiftf = _.bind(yshiftf, this, el, yzoomf)


      this.yzoom = yzoom = d3.behavior.zoom()
        .y(this.state.yscales)
        .scaleExtent([.1, 10000])
        .on('zoom', yzoomf);

      el.select('.axis.y').call(yzoom)
        .style('cursor', 'ns-resize')
      
      el.select('.yaxis')
        .on('mousedown.cstaty', yshiftf)



      if (!window.zoom) {
        window.zoom = yzoom;
        window.el = el;
        window.yzoomf = yzoomf
        window.yaxis = yaxis;
      }

      if (!util.isStr(this.model.get('type'))) {
        // sorry, don't support discrete zooming...

        var zoomf = function() {
          el.select('.axis.x').call(xaxis);
          el.selectAll('.mark') 
            .attr('x', function(d) {
              return d3.max([xscales.range()[0], xscales(d.range[0])]);
            })
            .attr('width', function(d) {
              var minx = d3.max([xscales.range()[0], xscales(d.range[0])]);
              if (xscales(d.range[1]) < minx) return 0;
              return d3.max([width, xscales(d.range[1]) - minx])
            })
            /*.style('display', function(d) {
              var x = xscales(d.val);
              var within = (x >= xscales.range()[0] && x <= xscales.range()[1]);
              return (within)? null : 'none';
            });*/
        }

        var zoom = d3.behavior.zoom()
          .x(xscales)
          .scaleExtent([.8, 1000])
          .on('zoom', zoomf)
        el.select('.axis.x').call(zoom)
          .style('cursor', 'ew-resize')

        var xStart = null;
        var curXScale = null;

        d3.select('body')
          .on('keydown', function() {
            
          })

        el.select('.xaxis')
          .on('mousedown.cstatx', function() {
            if (d3.event.shiftKey) {
              xStart = d3.event.x;
              curXScale = zoom.scale();
              d3.select('body')
                .on('mousemove.cstatx', function() {
                  var diff = ((d3.event.x - xStart) / 100);
                  if (diff >= 0) { 
                    diff += 1.0; 
                  } else if (diff < 0) { 
                    diff = 1.0 / (Math.abs(diff)+1);
                  }
                  zoom.scale(diff*curXScale);

                })
                .on('mouseup.cstatx', function() {
                  d3.select('body')
                    .on('mousemove.cstatx', null)
                    .on('mouseup.cstatx', null);
                });
            }
          })

      }

      return this;
    },



    renderPlot: function(svg) {
      svg.empty();
      this.d3svg = d3.select(svg.get()[0]);
      var c = this.d3svg
          .attr('class', 'cstat-container')
          .attr('width', this.state.w+this.state.lp)
          .attr('height', this.state.h+this.state.bp)
        .append('g')
          .attr('transform', "translate("+this.state.lp+", 0)")
          .attr('width', this.state.w)
          .attr('height', this.state.h)


      c.append('rect')
        .classed("plot-background", true)
        .attr('width', this.state.w)
        .attr('height', this.state.h)
        .attr('fill', 'none')
        .attr('stroke', 'none')
        .style('pointer-events', 'all')

      var dc = c.append('g')
        .attr('class', "cstat data-container")

      this.setupScales();
      this.renderAxes(c);
      this.renderData(dc);
      this.renderBrushes(dc);
      this.renderZoom(c);


    }
  });
});

