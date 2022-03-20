#!/usr/bin/nodejs

var express = require('express');
var https = require('https');
const { AuthorizationCode } = require('simple-oauth2');
var app = express();
var mysql = require('mysql');

var hbs = require('hbs');

var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

app.set('trust proxy', 1);
app.set('view engine', 'hbs');

var cookieParser = require('cookie-parser');
app.use(cookieParser());

var cookieSession = require('cookie-session');
app.use(cookieSession({
    name: 'tempcookie',
    keys: ['temp']
}));


var path = require('path');
const { config } = require('process');
console.log(__dirname);
app.use(express.static(path.join(__dirname,'static')));

//pages

app.get('/',function(req,res){
    res.render('homepage');
});

app.get('/python-test',function(req,res){
    res.render('python-test');
});


// -------------- listener -------------- //
// // The listener is what keeps node 'alive.' 

var listener = app.listen(5000, function() {
    console.log("Express server started");
});