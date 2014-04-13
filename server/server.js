var WALLPAPER_SERVER_PORT = 3102;

var WebSocketServer = require('ws').Server
  , wss = new WebSocketServer({port: 3101})
  , fs = require('fs');

var WALLPAPER_DIR = 'wallpapers/';

var WALLPAPER_SERVER_HOST = '0.0.0.0';

var http = require('http');
http.createServer(function (req, res) {
  console.log('HTTP REQUEST: ' + req.url);
  var filename = req.url.replace('/wallpaper/', '');
  var filePath = WALLPAPER_DIR + filename;
  if (filename === '') {
    fs.readdir(WALLPAPER_DIR, function(err, files) {
      if (err) { throw err; }  // (╯°□°)╯︵ ┻━┻
      res.end(JSON.stringify(files));
    });
  } else {
    try {
      var readStream = fs.createReadStream(filePath);
      readStream.pipe(res);
    } catch(err) {
      console.log('BAD REQUEST!');
      console.log(err);
      res.statusCode = 404;
      res.end({'error': 'Not found'});
    }
  }
}).listen(WALLPAPER_SERVER_PORT, WALLPAPER_SERVER_HOST);

var new_wallpaper = function(ws, filter) {
  // TODO: Apply filters to find the wallpaper.
  console.log('Requesting wallpaper with filter: ' + JSON.stringify(filter));
  if(filter.sfw) { console.log('Only searching for SFW wallpapers!'); }
  fs.readdir(WALLPAPER_DIR, function(err, files) {
    // TODO: Handle yo shit.
    if(err) { throw err; }
    var id = Math.floor((Math.random()*files.length));
    var filename = files[id];
    ws.send(JSON.stringify({'wallpaper_url': 'wallpaper/' + filename }));
  });
};

wss.on('connection', function(ws) {
    console.log('WS CONNECTION');
    var task;
    var initial = true;
    ws.on('message', function(message) {
      var data = JSON.parse(message);
      var filter = data.filter;
      var interval = data.interval;
      console.log("Sending a new wallpaper every " + interval + " seconds with the following filters: " + JSON.stringify(filter));
      if(task) { clearInterval(task); }
      // Run the wallpaper function once before getting into the timer since
      // it won't set the initial wallpaper.
      if(initial === true) {
        initial = false;
        new_wallpaper(ws, filter);
      }
      task = setInterval(new_wallpaper, interval*1000, ws, filter);
    });
});
