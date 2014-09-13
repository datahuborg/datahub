// 
define(function(require) {
  var Handlebars = require('handlebars'),
      Backbone = require('backbone'),
      d3 = require('d3'),
      $ = require('jquery'),
      util = require('summary/util');

  var Task = Backbone.Model.extend({
    defaults: function() {
      return {
        id: -1,
        text: "",
        options: [],      // [ "text", "text",... ]
        textbox: false,   // setting this to True overrides .options
        //largetextbox: false,
        truth: -1,        // a value or a function(answer, Task)
        answer: -1,
        successText: "Nice!  You'll see the next task in 2...1...",
        starttime: null,
        endtime: null
      }
    },

    validate: function() {
      var truth = this.get('truth'),
          answer = this.get('answer');

      if (_.isFunction(truth)) {
        return truth(answer, this);
      }
      if (this.get('textbox')) {
        return _.isEqual(
          String(truth).trim().toLowerCase(),
          String(answer).trim().toLowerCase()
        );
      } else {
        return truth == answer;
      }
    },

    toJSON: function() {
      var json = _.clone(this.attributes);
      json.options = _.map(json.options, function(text, idx) {
        return { text: text, idx: idx }
      });
      return json;
    }

  });

  return Backbone.View.extend({
    className: "task",

    events: {
      'click .submit':              'onSubmit',
      'keydown input[name=text]':   'onMouseDown',
      'click input[type=radio]':    'onOption'
    },

    template: Handlebars.compile($("#task-template").html()),

    initialize: function(attrs) {
      this.model = new Task(attrs);
      _.each((attrs.on || {}), function(f, name) {
        this.on(name, f);
      }, this);
    },

    onOption: function(ev) {
      var el = $(ev.target);
      var idx = el.val();
      this.model.set('answer', idx);
    },

    onMouseDown: function(ev) {
      //if (this.model.get('largetextbox'))
      this.model.set('answer', this.$("textarea[name=text]").val());
      //else
      //this.model.set('answer', this.$("input[name=text]").val());
    },


    onSubmit: function() {
      if (this.model.get('textbox')) {
        this.onMouseDown();
      }
      this.model.set('endtime', Date.now());

      this.trigger("trysubmit", this);

      var isvalid = this.model.validate();
      var text = "";
      if (isvalid == true) {
        text = this.model.get('successText') || "Nice job!";
        this.$(".error")
          .removeClass("bs-callout-danger")
          .addClass('bs-callout-info')
        this.trigger('submit', this);
      } else {
        if (_.isString(isvalid)) {
          text = this.model.get('failText') || isvalid;
        } else {
          text = this.model.get('failText') || "That answer doesn't seem right";
        }
      }

      //text = text + " " + localStorage['name'] + " " + ((this.model.get('endtime') - this.model.get('starttime'))/1000.);
      this.$(".error").text(text).show();
    },

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },

    show: function() {
      $(this.model.get('attachTo')).append(this.render().el);
      this.$el.show();
      this.model.set('starttime', Date.now())
      this.trigger('show', this);
    },

    hide: function() {
      this.$el.hide().remove();
      this.trigger('hide', this);
    }

  });
});
 
