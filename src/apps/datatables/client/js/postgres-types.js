var number_types = ["bigint", "int8", "bigserial", "serial8", "double precision", "float8", 
        "integer", "int", "int4", "real", "float4", "smallint", "int2", "serial", "serial4"];

var PostgresTypes = function() {
  var that = {};
  that.is_numeric = function(type) {
    return number_types.indexOf(type) !== -1;
  };


  that.can_apply = function(agg, type) {
    agg = agg.toLowerCase();
    if (agg === "sum" || agg === "avg") {
      return that.is_numeric(type);
    } 
    return true;
  };
  return that;
};

module.exports = PostgresTypes;
