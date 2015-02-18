var del = require("del");
var gulp = require("gulp");
var watch = require('gulp-watch');
var handlebars = require('gulp-handlebars');
var wrap = require('gulp-wrap');
var declare = require('gulp-declare');
var concat = require('gulp-concat');
var less = require('gulp-less');
var path = require('path');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');

var static_base = "../../browser/static/dataq/";

gulp.task("default", ["clean", "templates", "styles", "scripts", "index", "watch"]);

gulp.task('templates', ["clean"], function() {
  gulp.src("./client_src/templates/*.hbs")
    .pipe(handlebars())
    .on("error", function(err) { console.log(err.message) })
    .pipe(wrap("Handlebars.template(<%= contents %>)"))
    .pipe(declare({
      namespace: "DataQ.templates",
      noRedeclare: true
    }))
    .pipe(concat('templates.js'))
    .pipe(gulp.dest(static_base));
});

gulp.task('styles', ["clean"], function() {
  gulp.src("./client_src/less/*.less")
    .pipe(less({
      paths: [ path.join(__dirname, 'less', 'includes') ]
    }))
    .pipe(gulp.dest(static_base + 'css/'));
});

gulp.task("clean", function(cb) {
  del([
    static_base + "**"
  ], {force: true}, cb);
});

gulp.task("scripts", ["clean"], function() {
  gulp.src("./client_src/js/*.js")
    .pipe(sourcemaps.init())
    .pipe(concat("dataq.min.js"))
    .pipe(uglify())
    .on("error", function(err){console.log(err);})
    .pipe(sourcemaps.write("./"))
    .pipe(gulp.dest(static_base + "js/"))
});

gulp.task("index", ["clean"], function() {
  gulp.src("./client_src/index.html")
    .pipe(gulp.dest(static_base));
});

gulp.task("watch", ["clean"], function() {
  gulp.watch("./client_src/**/*.*", ["clean", "templates", "styles", "scripts", "index"]);
});
