const gulp = require('gulp')
var clean = require('gulp-clean')
const sass = require('gulp-sass')
const uglify = require('gulp-uglify')
const saveLicense = require('uglify-save-license')
const rename = require('gulp-rename')
const postcss = require('gulp-postcss')
const autoprefixer = require('autoprefixer')
const cssnano = require('cssnano')
const sourcemaps = require('gulp-sourcemaps')
const browserSync = require('browser-sync').create()
const argv = require('yargs').argv

const isBrowserSyncStatic = (argv.bsync_static === undefined) ? false : true


const InputDir = './src'
const StylesInputDir = InputDir.concat('/scss')
const StylesInputFiles = StylesInputDir.concat('/**/*.scss')
const ScriptsInputDir = InputDir.concat('/js')
const ScriptsInputFiles = ScriptsInputDir.concat('/**/*.js')

var OutputDir = './shortener_app/static/shortener_app'
if (isBrowserSyncStatic) {
    OutputDir = './dist'
}
const StylesOutputDir = OutputDir.concat('/css')
const ScriptsOutputDir = OutputDir.concat('/js')
const ScriptsOutputVendorDir = ScriptsOutputDir.concat('/vendor')
const ScriptsOutputSuffix = '.min'
const ScriptsVendorFiles = [
    'node_modules/bootstrap/dist/js/bootstrap.js',
    'node_modules/jquery/dist/jquery.js',
    'node_modules/popper.js/dist/umd/popper.js',
    'node_modules/clipboard/dist/clipboard.js',
    'node_modules/chart.js/dist/Chart.js',
]

var TemplateDir = './shortener_app/templates'
if (isBrowserSyncStatic) {
    TemplateDir = OutputDir
}
var TemplateFiles = TemplateDir.concat('/**/*.html')

const browserSyncProxyUrl = 'localhost:8000'
const browserSyncStaticDir = OutputDir


function cleanStyles(cb){
    return gulp.src([StylesOutputDir], {allowEmpty: true, read: false})
        .pipe(clean())
}

function cleanJavascript(cb){
    return gulp.src([ScriptsOutputDir], {allowEmpty: true, read: false})
        .pipe(clean())
}

function compileStyles(cb) {
    var postcssplugins = [
        autoprefixer({browsers: ['last 1 version']}),
        cssnano()
    ];

    return gulp.src([StylesInputFiles])
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(postcss(postcssplugins))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(StylesOutputDir))
        .pipe(browserSync.stream())
}

function vendorJavascript(cb) {
    return gulp.src(ScriptsVendorFiles)
        .pipe(sourcemaps.init())
        .pipe(uglify({
            output: {
                comments: saveLicense
            }
        }))
        .pipe(rename({ suffix: ScriptsOutputSuffix }))
        .pipe(sourcemaps.write('maps'))
        .pipe(gulp.dest(ScriptsOutputVendorDir))
        .pipe(browserSync.stream())
}

function compileJavascript(cb) {
    return gulp.src([ScriptsInputFiles])
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(rename({ suffix: ScriptsOutputSuffix }))
        .pipe(sourcemaps.write('maps'))
        .pipe(gulp.dest(ScriptsOutputDir))
        .pipe(browserSync.stream())
}

const buildStyles = gulp.series(cleanStyles, compileStyles)
const buildJavascript = gulp.series(cleanJavascript, vendorJavascript, compileJavascript)

function watchall(cb) {
    // Proxy server
    var browserSyncOptions = {
        proxy: browserSyncProxyUrl
    }

    // Static server
    if (isBrowserSyncStatic) {
        browserSyncOptions = {
            server: {
                baseDir: browserSyncStaticDir
            }
        }
    }
    browserSync.init(browserSyncOptions)

    gulp.watch([StylesInputFiles], buildStyles)
    gulp.watch([ScriptsInputFiles], buildJavascript)
    gulp.watch(TemplateFiles).on('change', browserSync.reload)
}

const build = gulp.parallel(buildStyles, buildJavascript)
var serve = gulp.series(build, watchall)

exports.build = build
exports.serve = serve
exports.default = serve
