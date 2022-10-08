
// flash.js
// Customizable jQuery library for web applications flash messages
// Author: Theodoros Georgopoulos
// Date: March 20, 2018
// Version: 1.0.0
// Copyright: MIT


// define the message container div
var $message_container = $("<div class='flash_color'></div>");
$('body').append($message_container);

// define the default options_flash
var $options_flash= {
  'bgColor' : '#5cb85c !important',
  'duration' : 5000,
  'ftColor' : 'white',
  'vPosition' : 'top',
  'hPosition' : 'right',
  'fadeIn' : 400,
  'fadeOut' : 400,
  'clickable' : true,
  'autohide' : true
};


function flash(message, options_flash = null){
  var type = typeof options_flash;
  if (options_flash !== null && type === 'object') {
    $.extend($options_flash, options_flash)
  }
//Message container div css
  msg_container_css = {
    "position": "fixed",
    "margin-left" : '7px',
    "z-index" : '50',
  };
  msg_container_css[$options_flash.vPosition] = "3px";
  msg_container_css[$options_flash.hPosition] = "5px";
  $message_container.css(msg_container_css);


// define the message div
var $message = $("<div class='shadow'></div>");

//Message div css
  msg_css = {
    'text-align' : 'right',
    'margin-top' : '10px',
    'padding' : '15px',
    'border' : '1px solid #dcdcdc',
    'border-radius': '5px',
    'float': 'right',
    'clear': 'right',
    'background-color': $options_flash.bgColor + ' !important',
    'color' : $options_flash.ftColor,
    'font-family': "Arial, Helvetica, sans-serif",
  };
  $message.css(msg_css);
//Adding text to message
  $message.text(message);

//Appeding message div to message container div
  $message_container.append($message).children(':last').hide().fadeIn($options_flash.fadeIn);
//Check if message is clickable to enable message click hide action
  if ($options_flash.clickable) {
    $message.on('click', function(){
      $(this).fadeOut($options_flash.fadeOut);
    });
  }

//Check if message is enabled to autohide
  if ($options_flash.autohide) {
    setTimeout(function(){
      $message.fadeOut($options_flash.fadeOut);
    },$options_flash.duration);
  }


};
$(".flash_color > div").css('background-color', $options_flash.bgColor+' !important');

