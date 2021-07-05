var Mouse = require("node-mouse");

var m = new Mouse();
//var m2 = new Mouse(8);
//var m3 = new Mouse(13);


m.on("mousedown", function(event) {
    console.log("1:", event)
});

/*m2.on("mousedown", function(event) {
    console.log("2:", event)
});

m3.on("mousedown", function(event) {
    console.log("3:", event)
});*/




m.on("mouseup", function(event) {
    console.log(event)
});


m.on("click", function(event) {
    console.log(event)
});

m.on("mousemove", function(event) {
    console.log(event)
});

