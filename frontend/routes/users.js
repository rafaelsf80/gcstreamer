var express = require('express');
var router = express.Router();

// localhost:3000/users 
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

// localhost:3000/users/new 
router.get('/new', function(req, res, next) {
  res.send('entrando en users/new');
});

// localhost:3000/users/usuario.doc
// localhost:3000/users/usuario.csv
// localhost:3000/users/usuario.xls
router.get('/usuario.:extension', function(req, res) {
  console.log(req.params)
  res.send('recuperamos usuario con extensión');
});

// localhost:3000/users/45 
router.get('/:userId', function(req, res) {
  console.log(req.params)
  res.render('usuario', {
    userId: req.params.userId
  })
  // res.send('respond with a userId ' + req.params.userId);
});

module.exports = router;
