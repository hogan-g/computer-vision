var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Class Vision' });
});

/* lecturer page that displays modules */
router.get('/lecturer', function(req, res, next){
  res.render('lecturer', { title: 'Lecturer'})
});

/* module page that displays lectures for that module */
router.get('/module', function(req, res, next){
  res.render('module', { title: 'Module' })
});

/* timetable page that displays all lectures chronologically */
router.get('/timetable', function(req, res, next){
  res.render('timetable', { title: 'Timetable' })
});

module.exports = router;
