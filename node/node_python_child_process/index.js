console.log('hello from index.js')

var spawn = require('child_process').spawn,
    ls    = spawn('python',['test.py']);

ls.stdout.on('data', function (data) {
    console.log('stdout: ' + data);
});

ls.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
});
