var Mouse = require("node-mouse");

var m = new Mouse(2);

m.on("mousedown", function(event) {
    console.log(event)
});


m.on("mouseup", function(event) {
    console.log(event)
});


m.on("click", function(event) {
    console.log(event)
});

m.on("mousemove", function(event) {
    console.log(event)
});


