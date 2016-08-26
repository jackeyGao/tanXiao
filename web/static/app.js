// File Name: static/app.js
// Author: JackeyGao
// mail: gaojunqi@outlook.com
// Created Time: 五  8/19 22:59:57 2016

Vue.config.delimiters = ['${', '}}']

var STORAGE_KEY = 'tasks';
var colors = [ 
  "green", "red", "yellow", "teal", 
  "orange", "black", "olive", "blue", 
  "violet", "purple", "pink", "brown", ""
  ]

var ref = new Wilddog("https://tanxiao.wilddogio.com/labels");

function getRandomInt(range, wt) {
    var range = range || 75
    var wt = wt || 2
    return Math.floor(Math.random() * range + wt)
}


Vue.transition('fade', {
  css: false,
  enter: function (el, done) {
    $(el)
      .css('opacity', 0)
      .animate({ opacity: 1 }, 1000, done)
  },
  enterCancelled: function (el) {
    $(el).stop()
  },
  leave: function (el, done) {
    // 与 enter 相同
    $(el).animate({ opacity: 0 }, 4000, done)
  },
  leaveCancelled: function (el) {
    $(el).stop()
  }
})

window.labels = []


var vm = new Vue({
  el: "#tanxiao",
  data: {
      newTitle: "",
      labels: window.labels,
  },
  methods: {
      addLabel: function() {
          var div = document.getElementById('tanxiao');
          var x = getRandomInt();
          var y = getRandomInt();
          var basic = Math.random() < 0.5 ? true : false;

          var value = this.newTitle && this.newTitle.trim();

          if (!value) {
              return;
          }

          if (value.length === 1) {
              var size = '3.8em';
          } else {
              var size = .7 + (4 / value.length) + 'em'
          }

          var color = colors[Math.floor(Math.random() * colors.length)]
          ref.push({ content: value, color: color, x: x + '%', y: y + '%', basic: basic, size: size});
          this.newTitle = "";

          if (this.labels.length > 20) {
            // 如果队列大于三十则去除最早的记
            this.labels.shift();
          }
      }
  },
})


ref.limitToLast(20).on("child_added", function(snapshot) {
  this.labels.push(snapshot.val());
}, function (errorObject) {
  console.log("The read failed: " + errorObject.code);
});

