// ScorpionView

define(function(require) {
  var Handlebars = require('handlebars'),
      Backbone = require('backbone'),
      d3 = require('d3'),
      $ = require('jquery'),
      md5 = require('md5'),
      util = require('summary/util'),
      ScorpionQuery = require('summary/scorpionquery'),
      StatusView = require('summary/status');

  var ScorpionView = Backbone.View.extend({
    template: Handlebars.compile($("#scorpion-template").html()),

    events: {
      "click #scorpion_submit":  "onSubmit",
      "click .close":            "onClose",
      "click #addbad":           "onAddBad",
      "click #addgood":          "onAddGood",
      "click #clearbad":         "onClearBad",
      "click #cleargood":        "onClearGood",
      "click #draw":             "onDrawToggle"

    },

    initialize: function(attrs) {
      this.queryview = attrs.queryview;
      this.donetext = "click when done drawing";
      this.drawtext = "click to draw expected values for selected results";

      this.listenTo(this.model, 'change', this.onChange);
    },

    onChange: function() {
      this.render();
      this.$el.show();
      return this;
    },

    onResult: function(resp) {
      var _this = this;
      $(".scorpion-wait").hide();
      if (this.statusview) {
        this.statusview.state.running = false;
        this.statusview.$el.remove();
        this.statusview = null;
      }

      // hide the partial results
      $("#scorpion-partialresults-container").fadeOut(500);
      $("#scorpion-results-container").fadeIn(500);
      this.model.get('partialresults').reset();


      //
      // ewu: I'm sorry for this ghetto hack to make sliders work
      //
      var top_k_results = resp.get('top_k_results');
      if (top_k_results && _.size(top_k_results)) {
        var c_vals = _.chain(top_k_results)
          .keys()
          .map(function(v) { return +v; })
          .sortBy()
          .value();
        var maxv = d3.max(c_vals),
            minv = d3.min(c_vals);
        var nearest_c = function(v) {
          var cs = _.filter(c_vals, function(c) { return c <= v; });
          var c = _.last(cs);
          return c;
        }
        $("#slider-container").show();
        var slider = $("#scorpion-slider");
        var prev_c = null;

        slider.slider({
            min: minv,
            max: maxv,
            step: (maxv - minv) / 100.0,
            formater: function(v) {
              return String(nearest_c(+v));
            } 
          })
          .on("slide", function() {
            var c = nearest_c(+slider.slider('getValue'));
            if (c == prev_c) return;
            _this.model.get('results').reset(top_k_results[c]);
            prev_c = c;
          });

        $("#scorpion-showbest")
          .off("click")
          .click(function() {
            _this.model.get('results').reset(_this.model.get('_results'));
          });
      }
      //
      // ewu: end ghetto hack
      //

      if (resp.get('errmsg')) {
        this.$("#errmsg").text(resp.errormsg);
      } else {
        this.$el.fadeOut();
        this.$("#errmsg").text("");
        this.trigger('scorpionquery:done');
      }

    },


    onSubmit: function() {
      if (!this.model.isValid()) {
        this.$("#errmsg").html(this.model.validationError);
        return false;
      }
      var _this = this;
      console.log(this.model.get('erreqs'));
      console.log(this.model.get('badselection'));

      var ignore_cols = $("input.errcol")
        .map(function(idx, el) { 
          if (!el.checked) return el.value;
        });
      ignore_cols = _.compact(ignore_cols);
      this.model.set('ignore_cols', ignore_cols);

      $(".scorpion-wait").show();
      try { $("#scorpion-slider").slider('destroy'); } catch(e) {}
      $("#scorpion-slider").hide();
      $("#slider-container").hide();

      $.get('/apps/dbwipes/api/requestid', function(resp) {
        var requestid = resp.requestid;
        console.log("got reqid " + requestid)
        _this.model.fetch({
          data: {
            fake: util.debugMode(),
            requestid: requestid,
            json: JSON.stringify(_this.model.toJSON()) ,
            username: window.username,
            db: _this.model.get('query').get('db')
          }, 
          //type: 'POST',
          success: _this.onResult.bind(_this),
          error: _this.onResult.bind(_this)
        });

      /*
        _this.statusview = new StatusView({ 
          requestid: requestid ,
          query: _this.model.get('query'),
          username: window.username,
          results: _this.model.get('partialresults')
        });
        _this.statusview.render();
        $("#scorpion_status").append(_this.statusview.$el);

        */
        $("#scorpion-results-container").fadeOut(500);
        $("#scorpion-partialresults-container").fadeIn(500);
      }, 'json')
    },

    onClose: function() {
      this.$el.hide();
    },
    onAddBad: function() {
      this.model.merge('badselection', this.model.get('selection'));
    },
    onAddGood: function() {
      this.model.merge('goodselection', this.model.get('selection'));
    },
    onClearBad: function() {
      this.model.set('badselection', {});
    },
    onClearGood: function() {
      this.model.set('goodselection', {});
    },
    onDrawToggle: function() {
      var draw = this.$("#draw")
          qv = this.queryview;
      
      if (qv.brushStatus() == 'all') {
        qv.disableBrush();
        qv.dv.enable();
        draw.addClass("drawing");
        draw.text(this.donetext);
      } else {
        qv.enableBrush();
        qv.dv.disable();
        draw.removeClass("drawing");
        draw.text(this.drawtext);
      }
    },

    render: function() {
      var _this = this,
          model = this.model;

      this.$el.attr("id", "walkthrough-container");
      this.$el.empty().html(this.template(this.model.toJSON()));

      var draw = this.$("#draw");
      var qv = this.queryview;
      draw.text((qv.brushStatus() == 'all')? this.drawtext : this.donetext);

      return this;
    },


  });

  return ScorpionView;
});

