var WALLPAPER_SERVER_PORT = 3102;

var WebSocketServer = require('ws').Server
  , wss = new WebSocketServer({port: 3101})
  , fs = require('fs');

var WALLPAPER_DIR = 'wallpapers/';

var WALLPAPER_SERVER_HOST = '0.0.0.0';

var http = require('http');
http.createServer(function (req, res) {
  console.log('HTTP REQUEST');
  var filename = req.url.replace('/wallpaper/', '');
  var filePath = WALLPAPER_DIR + filename;
  var readStream = fs.createReadStream(filePath);
  readStream.pipe(res);
}).listen(WALLPAPER_SERVER_PORT, WALLPAPER_SERVER_HOST);

wss.on('connection', function(ws) {
    console.log('WS CONNECTION');
    ws.on('message', function(message) {
      var data = JSON.parse(message);
      if(data.request === 'wallpaper') {
        // TODO: Apply filters to find the wallpaper.
        console.log('Requesting wallpaper');
        fs.readdir(WALLPAPER_DIR, function(err, files) {
          // TODO: Handle yo shit.
          if(err) { throw err; }
          var id = Math.floor((Math.random()*files.length)+1);
          var filename = files[id];
          ws.send(JSON.stringify({'wallpaper_url': 'wallpaper/' + filename }));
        });
      }
    });
});
