var del = require('del');
var gulp = require('gulp');
var watch = require('gulp-watch');
var handlebars = require('gulp-handlebars'); // must use v3.0.1 (4.0.0 failed)
var wrap = require('gulp-wrap');
var declare = require('gulp-declare');
var concat = require('gulp-concat');
var less = require('gulp-less');
var path = require('path');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');

var static_base = '../../browser/static/dataq/';

// 'gulp' rebuilds all files
gulp.task('default', ['templates', 'styles', 'scripts', 'index']);

gulp.task('templates', function() {
  gulp.src('./client_src/templates/*.hbs')
    .pipe(handlebars())
    .on('error', function(err) { console.log(err.message) })
    .pipe(wrap('Handlebars.template(<%= contents %>)'))
    .pipe(declare({
      namespace: 'DataQ.templates',
      noRedeclare: true
    }))
    .pipe(concat('templates.js'))
    .pipe(gulp.dest(static_base));
});

gulp.task('styles', function() {
  gulp.src('./client_src/less/*.less')
    .pipe(less({
      paths: [path.join(__dirname, 'less', 'includes')]
    }))
    .pipe(gulp.dest(static_base + 'css/'));
});

gulp.task('scripts', function() {
  gulp.src('./client_src/js/*.js')
    .pipe(sourcemaps.init())
    .pipe(concat('dataq.min.js'))
    .pipe(uglify())
    .on('error', function(err) {console.log(err);})
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(static_base + 'js/'));
});

gulp.task('index', function() {
  gulp.src('./client_src/index.html')
    .pipe(gulp.dest(static_base));
});

// 'gulp clean' removes all files
gulp.task('clean', function() {
  del([
    static_base + '**'
  ], {force: true});
});

// 'gulp watch' builds files automatically as they are modifed
gulp.task('watch', function() {
  gulp.watch('./client_src/templates/*.hbs', function() {
    gulp.run('templates');
  });
  gulp.watch('./client_src/less/*.less', function() {
    gulp.run('styles');
  });
  gulp.watch('./client_src/js/*.js', function() {
    gulp.run('scripts');
  });
  gulp.watch('./client_src/index.html', function() {
    gulp.run('index');
  });
});
