define(function(require) {
  var Handlebars = require('handlebars'),
      Backbone = require('backbone'),
      d3 = require('d3'),
      $ = require('jquery'),
      ScorpionResult = require('summary/scorpionresult');
  
  var Status = Backbone.Model.extend({
    url: '/api/status',

    defaults: function() {
      return {
        requestid: null,
        results: null,  // scorpion results object
        prev_hash: null,
        status: ''
      };
    },

    initialize: function() {
    },
    
    parse: function(resp) {
      var results = this.get('results'),
          query = this.get('query');

      if (resp.results) {
        if (!_.isEqual(resp.hash, this.get('prev_hash'))) {
          var newresults = _.map(resp.results, function(r) {
            r.query = query;
            r.partial = true;
            return new ScorpionResult(r);
          });

          results.reset(newresults);
          console.log(["status parsed temporary response", resp])
        }

        this.set('prev_hash', resp.hash)
        resp.results = results;
      }
      return resp;
    },

    toJSON: function() {
      return {
        requestid: this.get('requestid')
      };
    }
  });

  var StatusView = Backbone.View.extend({
    tagName: 'div',
    initialize: function(attrs) {
      this.state = { running: true };
      this.model = new Status(attrs);
      this.listenTo(this.model, "change", this.render.bind(this));
      this.loadStatus();
    },
  
    loadStatus: function() {
      if (!this.state.running) {
        this.model.set('status', '');
        return;
      }
     var onSuccess = (function() {
        _.delay(this.loadStatus.bind(this), 1000)
      }).bind(this) ;

      this.model.fetch({
        data: this.model.toJSON(),
        success: onSuccess,
        error: onSuccess
      })
    },

    render: function() {
      var span = this.$el.append("span")
      span
        .addClass("status")
        .text(this.model.get('status'))
      return this;
    }
  });
  return StatusView;
});

 
