'use strict';

var browserify = require('browserify');
var stringify = require("stringify");
var gulp = require('gulp');
var transform = require('vinyl-transform');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var del = require("del");
var source = require('vinyl-source-stream');
var hbsfy = require("hbsfy").configure({
  extensions: ["hbs", "html"]
});

var destination = "../../browser/static/datatables/";

gulp.task('clean', function(cb) {
  del([destination], {"force": true}, cb);
});

gulp.task('browserify', ['clean'], function() {
  var bundleMethod = browserify;//global.isWatching ? watchify : browserify;
 
  var bundler = bundleMethod({
    // Specify the entry point of your app
    entries: ['./client/js/dataTables.extra.js']
  });
 
  var bundle = function() {
    return bundler
      .transform(hbsfy)
      // Enable source maps!
      .bundle()
      // Use vinyl-source-stream to make the
      // stream gulp compatible. Specifiy the
      // desired output filename here.
      .pipe(source('dataTables.extra.js'))
      // Specify the output destination
      .pipe(gulp.dest(destination + "js"));
  };
 
  return bundle();
});

gulp.task("styles", ['clean'], function() {
  gulp.src('./client/css/dataTables.bootstrap.extra.css')
  .pipe(gulp.dest(destination + "css"));
});
 
gulp.task('default', ['clean', 'browserify', 'styles']);
