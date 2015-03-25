(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var api = require("./api.js");
var FilterBar = require("./filter-bar.js");

$.fn.EnhancedDataTable = function(repo, table) {
  // The jquer object for which the EnhancedDataTable function was triggered.
  var jqueryObject = this;
  var filterBar;

  // Get the column definitions for this table.
  api.get_column_definitions(repo, table, function(err, columnDefs) {
    if (err !== null) {
      console.log("Failed to get column defs");
      return;
    }

    // Create the DataTable.
    var datatable = jqueryObject.DataTable({
      "dom": 'RC<"clear">lfrtip',
      "columnDefs": columnDefs,
      "searching": false,
      "scrollX": true,
      "serverSide": true,
      "colVis": {
        "overlayFade": 0,
        "stateChange": function(colName, visibility) {
        }
      },
      "ajax": {
        "url": api.table_url(repo, table),
        "data": function(d) {
          if (filterBar !== undefined) {
            d["filters"] = filterBar.filters();
            d["filterInverted"] = filterBar.isInverted();
          }
        }
      },
      "initComplete": function(settings, json) {
        filterBar = FilterBar(jqueryObject.parent().parent(), columnDefs, datatable);
      },
      "drawCallback": function(settings) {
        //console.log(datatable.ajax.json());
      }
    });
  });

  return this;
};

},{"./api.js":2,"./filter-bar.js":3}],2:[function(require,module,exports){
/**
 * This file contains the code for interacting with the API
 * for server side processing of datatables.
 */

// The root of the API.
var url_base = "/apps/datatables/api/";


// The object that will contain the API functions.
var api = {};


/**
 * Given a repo name and table name, construct the URL
 * which DataTables.js should request in order to get a
 * table draw.
 */
api.table_url = function(repo, table) {
  return url_base + "table/" + repo + "/" + table + "/";
}

/**
 * Given a repo name and table name, determine the schema of the table
 * and return a columnDefs (https://datatables.net/reference/option/columnDefs)
 * which is usable by DataTables.
 *
 * The callback is triggered as callback(err, columnDefs), where columnDefs is a
 * columnDef configuration for DataTables. If there is no error, err will be null.
 * Otherwise, it is a string indicating the error.
 */
api.get_column_definitions = function(repo, table, callback) {
  // Create the endpoint URL.
  var url = url_base + "schema/" + repo + "/" + table + "/";

  // Get the schema.
  $.get(url, function(schema_result) {

    // Parse if there's a success.
    if (schema_result.success) {
      var schema = schema_result.schema;
      var columnDefinitions = [];

      // Create the columnDefs.
      schema.forEach(function(column, index) {
        columnDefinitions.push({
          "name": column[0],
          "targets": index
        });
      });

      // Trigger the callback.
      callback(null, columnDefinitions);
    } else {
      callback("Failed columnDefs request");
    }
  });
}

module.exports = api;

},{}],3:[function(require,module,exports){
var filter_buttons_template = require("./templates/filter_buttons.hbs");
var filter_template = require("./templates/filter.hbs");

var nextOp = {
  "=": "!=",
  "!=": "<",
  "<": "<=",
  "<=": ">",
  ">": ">=",
  ">=": "btw a;b",
  "btw a;b": "="
};

$(document).on("click", ".dt-op-button", function() {
  $(this).text(nextOp[$(this).text()]);
  datatable.draw();
});

$(document).on("click", ".dt-invert-filter", function() {
  datatable.draw();
});

$(document).on("click", ".dt-new-filter", function() {
  createFilter();
});

$(document).on("click", ".dt-delete-button", function() {
  // Delete the entire row.
  // button < span < div < th < tr
  $(this).parent().parent().parent().parent().remove();
});

$(document).on("keyup change", ".dt-filter input[type=text]", function() {
  datatable.draw();
});

var createFilter = function(){
  var selector = $(".dataTables_scrollHeadInner thead"); 
  var order = datatable.colReorder.order();

  for (var i = 0; i < order.length; i++) {
    for (var j = 0; j < colDefs.length; j++) {
      if (colDefs[j].targets === order[i]) {
        colDefs[j].order = i;
      }
    }
  }

  colDefs.sort(function(a, b) {
    if (a.order < b.order) {
      return -1;
    } else if (a.order > b.order) {
      return 1;
    } else {
      return 0;
    }
  });

  selector.prepend(filter_template({"colDefs": colDefs}))

}

var colDefs;
var jqueryContainer;
var datatable;
module.exports = function(container, cd, dt) {
  var that = {};

  jqueryContainer = container;
  colDefs = cd;
  datatable = dt;
  jqueryContainer.after(filter_buttons_template());

  that.filters = function() {
    var filters = [];
    $(".dt-filter").each(function() {
      var filter = [];
      $(this).find("th").each(function() {
        var colname = $(this).data("colname");
        var filter_text = $(this).find("input[type=text]").val();
        var filter_op = $(this).find(".dt-op-button").text();
        
        // Sometimes DataTables.js will create duplicate copies of the filters. If so,
        // then we cannot extract the desired values, so we skip this "false filter".
        if (filter_text === undefined) {
          return;
        }

        if (filter_text.length > 0) {
          filter.push({
            "colname": colname,
            "filter_text": filter_text,
            "filter_op": filter_op
          });
        }
      });
      if (filter.length > 0) {
        filters.push(filter);
      }
    });
    return filters;
  };

  that.isInverted = function() {
    return $(".dt-invert-filter").prop("checked");
  };

  return that;
};

},{"./templates/filter.hbs":4,"./templates/filter_buttons.hbs":5}],4:[function(require,module,exports){
// hbsfy compiled Handlebars template
var HandlebarsCompiler = require('hbsfy/runtime');
module.exports = HandlebarsCompiler.template({"1":function(depth0,helpers,partials,data) {
    var stack1, helper, alias1=helpers.helperMissing, alias2="function", alias3=this.escapeExpression;

  return "    <th data-colname=\""
    + alias3(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"name","hash":{},"data":data}) : helper)))
    + "\">\n      <div class=\"input-group\">\n        <span class=\"input-group-btn\">\n"
    + ((stack1 = helpers['if'].call(depth0,(data && data.first),{"name":"if","hash":{},"fn":this.program(2, data, 0),"inverse":this.noop,"data":data})) != null ? stack1 : "")
    + "          <button class=\"btn btn-default dt-op-button\" type=\"button\">=</button>\n        </span>\n        <input type=\"text\" class=\"form-control dt-filtertext\" placeholder=\""
    + alias3(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"name","hash":{},"data":data}) : helper)))
    + "\"> \n      </div>\n    </th>\n";
},"2":function(depth0,helpers,partials,data) {
    return "          <button class=\"btn btn-danger dt-delete-button\" type=\"button\"><i class=\"fa fa-trash\"></i></button>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
    var stack1;

  return "<tr class=\"dt-filter\">\n"
    + ((stack1 = helpers.each.call(depth0,(depth0 != null ? depth0.colDefs : depth0),{"name":"each","hash":{},"fn":this.program(1, data, 0),"inverse":this.noop,"data":data})) != null ? stack1 : "")
    + "</tr>\n";
},"useData":true});

},{"hbsfy/runtime":13}],5:[function(require,module,exports){
// hbsfy compiled Handlebars template
var HandlebarsCompiler = require('hbsfy/runtime');
module.exports = HandlebarsCompiler.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
    return "<button class=\"btn btn-primary dt-new-filter\">New Filter</button>\n<label class=\"btn btn-primary\">\n  <input class=\"dt-invert-filter\" type=\"checkbox\" autocomplete=\"off\"> Invert Filter\n</label>\n";
},"useData":true});

},{"hbsfy/runtime":13}],6:[function(require,module,exports){
(function (global){
"use strict";
/*globals Handlebars: true */
var base = require("./handlebars/base");

// Each of these augment the Handlebars object. No need to setup here.
// (This is done to easily share code between commonjs and browse envs)
var SafeString = require("./handlebars/safe-string")["default"];
var Exception = require("./handlebars/exception")["default"];
var Utils = require("./handlebars/utils");
var runtime = require("./handlebars/runtime");

// For compatibility and usage outside of module systems, make the Handlebars object a namespace
var create = function() {
  var hb = new base.HandlebarsEnvironment();

  Utils.extend(hb, base);
  hb.SafeString = SafeString;
  hb.Exception = Exception;
  hb.Utils = Utils;
  hb.escapeExpression = Utils.escapeExpression;

  hb.VM = runtime;
  hb.template = function(spec) {
    return runtime.template(spec, hb);
  };

  return hb;
};

var Handlebars = create();
Handlebars.create = create;

/*jshint -W040 */
/* istanbul ignore next */
var root = typeof global !== 'undefined' ? global : window,
    $Handlebars = root.Handlebars;
/* istanbul ignore next */
Handlebars.noConflict = function() {
  if (root.Handlebars === Handlebars) {
    root.Handlebars = $Handlebars;
  }
};

Handlebars['default'] = Handlebars;

exports["default"] = Handlebars;
}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{"./handlebars/base":7,"./handlebars/exception":8,"./handlebars/runtime":9,"./handlebars/safe-string":10,"./handlebars/utils":11}],7:[function(require,module,exports){
"use strict";
var Utils = require("./utils");
var Exception = require("./exception")["default"];

var VERSION = "3.0.1";
exports.VERSION = VERSION;var COMPILER_REVISION = 6;
exports.COMPILER_REVISION = COMPILER_REVISION;
var REVISION_CHANGES = {
  1: '<= 1.0.rc.2', // 1.0.rc.2 is actually rev2 but doesn't report it
  2: '== 1.0.0-rc.3',
  3: '== 1.0.0-rc.4',
  4: '== 1.x.x',
  5: '== 2.0.0-alpha.x',
  6: '>= 2.0.0-beta.1'
};
exports.REVISION_CHANGES = REVISION_CHANGES;
var isArray = Utils.isArray,
    isFunction = Utils.isFunction,
    toString = Utils.toString,
    objectType = '[object Object]';

function HandlebarsEnvironment(helpers, partials) {
  this.helpers = helpers || {};
  this.partials = partials || {};

  registerDefaultHelpers(this);
}

exports.HandlebarsEnvironment = HandlebarsEnvironment;HandlebarsEnvironment.prototype = {
  constructor: HandlebarsEnvironment,

  logger: logger,
  log: log,

  registerHelper: function(name, fn) {
    if (toString.call(name) === objectType) {
      if (fn) { throw new Exception('Arg not supported with multiple helpers'); }
      Utils.extend(this.helpers, name);
    } else {
      this.helpers[name] = fn;
    }
  },
  unregisterHelper: function(name) {
    delete this.helpers[name];
  },

  registerPartial: function(name, partial) {
    if (toString.call(name) === objectType) {
      Utils.extend(this.partials,  name);
    } else {
      if (typeof partial === 'undefined') {
        throw new Exception('Attempting to register a partial as undefined');
      }
      this.partials[name] = partial;
    }
  },
  unregisterPartial: function(name) {
    delete this.partials[name];
  }
};

function registerDefaultHelpers(instance) {
  instance.registerHelper('helperMissing', function(/* [args, ]options */) {
    if(arguments.length === 1) {
      // A missing field in a {{foo}} constuct.
      return undefined;
    } else {
      // Someone is actually trying to call something, blow up.
      throw new Exception("Missing helper: '" + arguments[arguments.length-1].name + "'");
    }
  });

  instance.registerHelper('blockHelperMissing', function(context, options) {
    var inverse = options.inverse,
        fn = options.fn;

    if(context === true) {
      return fn(this);
    } else if(context === false || context == null) {
      return inverse(this);
    } else if (isArray(context)) {
      if(context.length > 0) {
        if (options.ids) {
          options.ids = [options.name];
        }

        return instance.helpers.each(context, options);
      } else {
        return inverse(this);
      }
    } else {
      if (options.data && options.ids) {
        var data = createFrame(options.data);
        data.contextPath = Utils.appendContextPath(options.data.contextPath, options.name);
        options = {data: data};
      }

      return fn(context, options);
    }
  });

  instance.registerHelper('each', function(context, options) {
    if (!options) {
      throw new Exception('Must pass iterator to #each');
    }

    var fn = options.fn, inverse = options.inverse;
    var i = 0, ret = "", data;

    var contextPath;
    if (options.data && options.ids) {
      contextPath = Utils.appendContextPath(options.data.contextPath, options.ids[0]) + '.';
    }

    if (isFunction(context)) { context = context.call(this); }

    if (options.data) {
      data = createFrame(options.data);
    }

    function execIteration(key, i, last) {
      if (data) {
        data.key = key;
        data.index = i;
        data.first = i === 0;
        data.last  = !!last;

        if (contextPath) {
          data.contextPath = contextPath + key;
        }
      }

      ret = ret + fn(context[key], {
        data: data,
        blockParams: Utils.blockParams([context[key], key], [contextPath + key, null])
      });
    }

    if(context && typeof context === 'object') {
      if (isArray(context)) {
        for(var j = context.length; i<j; i++) {
          execIteration(i, i, i === context.length-1);
        }
      } else {
        var priorKey;

        for(var key in context) {
          if(context.hasOwnProperty(key)) {
            // We're running the iterations one step out of sync so we can detect
            // the last iteration without have to scan the object twice and create
            // an itermediate keys array. 
            if (priorKey) {
              execIteration(priorKey, i-1);
            }
            priorKey = key;
            i++;
          }
        }
        if (priorKey) {
          execIteration(priorKey, i-1, true);
        }
      }
    }

    if(i === 0){
      ret = inverse(this);
    }

    return ret;
  });

  instance.registerHelper('if', function(conditional, options) {
    if (isFunction(conditional)) { conditional = conditional.call(this); }

    // Default behavior is to render the positive path if the value is truthy and not empty.
    // The `includeZero` option may be set to treat the condtional as purely not empty based on the
    // behavior of isEmpty. Effectively this determines if 0 is handled by the positive path or negative.
    if ((!options.hash.includeZero && !conditional) || Utils.isEmpty(conditional)) {
      return options.inverse(this);
    } else {
      return options.fn(this);
    }
  });

  instance.registerHelper('unless', function(conditional, options) {
    return instance.helpers['if'].call(this, conditional, {fn: options.inverse, inverse: options.fn, hash: options.hash});
  });

  instance.registerHelper('with', function(context, options) {
    if (isFunction(context)) { context = context.call(this); }

    var fn = options.fn;

    if (!Utils.isEmpty(context)) {
      if (options.data && options.ids) {
        var data = createFrame(options.data);
        data.contextPath = Utils.appendContextPath(options.data.contextPath, options.ids[0]);
        options = {data:data};
      }

      return fn(context, options);
    } else {
      return options.inverse(this);
    }
  });

  instance.registerHelper('log', function(message, options) {
    var level = options.data && options.data.level != null ? parseInt(options.data.level, 10) : 1;
    instance.log(level, message);
  });

  instance.registerHelper('lookup', function(obj, field) {
    return obj && obj[field];
  });
}

var logger = {
  methodMap: { 0: 'debug', 1: 'info', 2: 'warn', 3: 'error' },

  // State enum
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  level: 1,

  // Can be overridden in the host environment
  log: function(level, message) {
    if (typeof console !== 'undefined' && logger.level <= level) {
      var method = logger.methodMap[level];
      (console[method] || console.log).call(console, message);
    }
  }
};
exports.logger = logger;
var log = logger.log;
exports.log = log;
var createFrame = function(object) {
  var frame = Utils.extend({}, object);
  frame._parent = object;
  return frame;
};
exports.createFrame = createFrame;
},{"./exception":8,"./utils":11}],8:[function(require,module,exports){
"use strict";

var errorProps = ['description', 'fileName', 'lineNumber', 'message', 'name', 'number', 'stack'];

function Exception(message, node) {
  var loc = node && node.loc,
      line,
      column;
  if (loc) {
    line = loc.start.line;
    column = loc.start.column;

    message += ' - ' + line + ':' + column;
  }

  var tmp = Error.prototype.constructor.call(this, message);

  // Unfortunately errors are not enumerable in Chrome (at least), so `for prop in tmp` doesn't work.
  for (var idx = 0; idx < errorProps.length; idx++) {
    this[errorProps[idx]] = tmp[errorProps[idx]];
  }

  if (loc) {
    this.lineNumber = line;
    this.column = column;
  }
}

Exception.prototype = new Error();

exports["default"] = Exception;
},{}],9:[function(require,module,exports){
"use strict";
var Utils = require("./utils");
var Exception = require("./exception")["default"];
var COMPILER_REVISION = require("./base").COMPILER_REVISION;
var REVISION_CHANGES = require("./base").REVISION_CHANGES;
var createFrame = require("./base").createFrame;

function checkRevision(compilerInfo) {
  var compilerRevision = compilerInfo && compilerInfo[0] || 1,
      currentRevision = COMPILER_REVISION;

  if (compilerRevision !== currentRevision) {
    if (compilerRevision < currentRevision) {
      var runtimeVersions = REVISION_CHANGES[currentRevision],
          compilerVersions = REVISION_CHANGES[compilerRevision];
      throw new Exception("Template was precompiled with an older version of Handlebars than the current runtime. "+
            "Please update your precompiler to a newer version ("+runtimeVersions+") or downgrade your runtime to an older version ("+compilerVersions+").");
    } else {
      // Use the embedded version info since the runtime doesn't know about this revision yet
      throw new Exception("Template was precompiled with a newer version of Handlebars than the current runtime. "+
            "Please update your runtime to a newer version ("+compilerInfo[1]+").");
    }
  }
}

exports.checkRevision = checkRevision;// TODO: Remove this line and break up compilePartial

function template(templateSpec, env) {
  /* istanbul ignore next */
  if (!env) {
    throw new Exception("No environment passed to template");
  }
  if (!templateSpec || !templateSpec.main) {
    throw new Exception('Unknown template object: ' + typeof templateSpec);
  }

  // Note: Using env.VM references rather than local var references throughout this section to allow
  // for external users to override these as psuedo-supported APIs.
  env.VM.checkRevision(templateSpec.compiler);

  var invokePartialWrapper = function(partial, context, options) {
    if (options.hash) {
      context = Utils.extend({}, context, options.hash);
    }

    partial = env.VM.resolvePartial.call(this, partial, context, options);
    var result = env.VM.invokePartial.call(this, partial, context, options);

    if (result == null && env.compile) {
      options.partials[options.name] = env.compile(partial, templateSpec.compilerOptions, env);
      result = options.partials[options.name](context, options);
    }
    if (result != null) {
      if (options.indent) {
        var lines = result.split('\n');
        for (var i = 0, l = lines.length; i < l; i++) {
          if (!lines[i] && i + 1 === l) {
            break;
          }

          lines[i] = options.indent + lines[i];
        }
        result = lines.join('\n');
      }
      return result;
    } else {
      throw new Exception("The partial " + options.name + " could not be compiled when running in runtime-only mode");
    }
  };

  // Just add water
  var container = {
    strict: function(obj, name) {
      if (!(name in obj)) {
        throw new Exception('"' + name + '" not defined in ' + obj);
      }
      return obj[name];
    },
    lookup: function(depths, name) {
      var len = depths.length;
      for (var i = 0; i < len; i++) {
        if (depths[i] && depths[i][name] != null) {
          return depths[i][name];
        }
      }
    },
    lambda: function(current, context) {
      return typeof current === 'function' ? current.call(context) : current;
    },

    escapeExpression: Utils.escapeExpression,
    invokePartial: invokePartialWrapper,

    fn: function(i) {
      return templateSpec[i];
    },

    programs: [],
    program: function(i, data, declaredBlockParams, blockParams, depths) {
      var programWrapper = this.programs[i],
          fn = this.fn(i);
      if (data || depths || blockParams || declaredBlockParams) {
        programWrapper = program(this, i, fn, data, declaredBlockParams, blockParams, depths);
      } else if (!programWrapper) {
        programWrapper = this.programs[i] = program(this, i, fn);
      }
      return programWrapper;
    },

    data: function(data, depth) {
      while (data && depth--) {
        data = data._parent;
      }
      return data;
    },
    merge: function(param, common) {
      var ret = param || common;

      if (param && common && (param !== common)) {
        ret = Utils.extend({}, common, param);
      }

      return ret;
    },

    noop: env.VM.noop,
    compilerInfo: templateSpec.compiler
  };

  var ret = function(context, options) {
    options = options || {};
    var data = options.data;

    ret._setup(options);
    if (!options.partial && templateSpec.useData) {
      data = initData(context, data);
    }
    var depths,
        blockParams = templateSpec.useBlockParams ? [] : undefined;
    if (templateSpec.useDepths) {
      depths = options.depths ? [context].concat(options.depths) : [context];
    }

    return templateSpec.main.call(container, context, container.helpers, container.partials, data, blockParams, depths);
  };
  ret.isTop = true;

  ret._setup = function(options) {
    if (!options.partial) {
      container.helpers = container.merge(options.helpers, env.helpers);

      if (templateSpec.usePartial) {
        container.partials = container.merge(options.partials, env.partials);
      }
    } else {
      container.helpers = options.helpers;
      container.partials = options.partials;
    }
  };

  ret._child = function(i, data, blockParams, depths) {
    if (templateSpec.useBlockParams && !blockParams) {
      throw new Exception('must pass block params');
    }
    if (templateSpec.useDepths && !depths) {
      throw new Exception('must pass parent depths');
    }

    return program(container, i, templateSpec[i], data, 0, blockParams, depths);
  };
  return ret;
}

exports.template = template;function program(container, i, fn, data, declaredBlockParams, blockParams, depths) {
  var prog = function(context, options) {
    options = options || {};

    return fn.call(container,
        context,
        container.helpers, container.partials,
        options.data || data,
        blockParams && [options.blockParams].concat(blockParams),
        depths && [context].concat(depths));
  };
  prog.program = i;
  prog.depth = depths ? depths.length : 0;
  prog.blockParams = declaredBlockParams || 0;
  return prog;
}

exports.program = program;function resolvePartial(partial, context, options) {
  if (!partial) {
    partial = options.partials[options.name];
  } else if (!partial.call && !options.name) {
    // This is a dynamic partial that returned a string
    options.name = partial;
    partial = options.partials[partial];
  }
  return partial;
}

exports.resolvePartial = resolvePartial;function invokePartial(partial, context, options) {
  options.partial = true;

  if(partial === undefined) {
    throw new Exception("The partial " + options.name + " could not be found");
  } else if(partial instanceof Function) {
    return partial(context, options);
  }
}

exports.invokePartial = invokePartial;function noop() { return ""; }

exports.noop = noop;function initData(context, data) {
  if (!data || !('root' in data)) {
    data = data ? createFrame(data) : {};
    data.root = context;
  }
  return data;
}
},{"./base":7,"./exception":8,"./utils":11}],10:[function(require,module,exports){
"use strict";
// Build out our basic SafeString type
function SafeString(string) {
  this.string = string;
}

SafeString.prototype.toString = SafeString.prototype.toHTML = function() {
  return "" + this.string;
};

exports["default"] = SafeString;
},{}],11:[function(require,module,exports){
"use strict";
/*jshint -W004 */
var escape = {
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#x27;",
  "`": "&#x60;"
};

var badChars = /[&<>"'`]/g;
var possible = /[&<>"'`]/;

function escapeChar(chr) {
  return escape[chr];
}

function extend(obj /* , ...source */) {
  for (var i = 1; i < arguments.length; i++) {
    for (var key in arguments[i]) {
      if (Object.prototype.hasOwnProperty.call(arguments[i], key)) {
        obj[key] = arguments[i][key];
      }
    }
  }

  return obj;
}

exports.extend = extend;var toString = Object.prototype.toString;
exports.toString = toString;
// Sourced from lodash
// https://github.com/bestiejs/lodash/blob/master/LICENSE.txt
var isFunction = function(value) {
  return typeof value === 'function';
};
// fallback for older versions of Chrome and Safari
/* istanbul ignore next */
if (isFunction(/x/)) {
  isFunction = function(value) {
    return typeof value === 'function' && toString.call(value) === '[object Function]';
  };
}
var isFunction;
exports.isFunction = isFunction;
/* istanbul ignore next */
var isArray = Array.isArray || function(value) {
  return (value && typeof value === 'object') ? toString.call(value) === '[object Array]' : false;
};
exports.isArray = isArray;
// Older IE versions do not directly support indexOf so we must implement our own, sadly.
function indexOf(array, value) {
  for (var i = 0, len = array.length; i < len; i++) {
    if (array[i] === value) {
      return i;
    }
  }
  return -1;
}

exports.indexOf = indexOf;
function escapeExpression(string) {
  if (typeof string !== 'string') {
    // don't escape SafeStrings, since they're already safe
    if (string && string.toHTML) {
      return string.toHTML();
    } else if (string == null) {
      return '';
    } else if (!string) {
      return string + '';
    }

    // Force a string conversion as this will be done by the append regardless and
    // the regex test will do this transparently behind the scenes, causing issues if
    // an object's to string has escaped characters in it.
    string = '' + string;
  }

  if (!possible.test(string)) { return string; }
  return string.replace(badChars, escapeChar);
}

exports.escapeExpression = escapeExpression;function isEmpty(value) {
  if (!value && value !== 0) {
    return true;
  } else if (isArray(value) && value.length === 0) {
    return true;
  } else {
    return false;
  }
}

exports.isEmpty = isEmpty;function blockParams(params, ids) {
  params.path = ids;
  return params;
}

exports.blockParams = blockParams;function appendContextPath(contextPath, id) {
  return (contextPath ? contextPath + '.' : '') + id;
}

exports.appendContextPath = appendContextPath;
},{}],12:[function(require,module,exports){
// Create a simple path alias to allow browserify to resolve
// the runtime on a supported path.
module.exports = require('./dist/cjs/handlebars.runtime')['default'];

},{"./dist/cjs/handlebars.runtime":6}],13:[function(require,module,exports){
module.exports = require("handlebars/runtime")["default"];

},{"handlebars/runtime":12}]},{},[1]);
