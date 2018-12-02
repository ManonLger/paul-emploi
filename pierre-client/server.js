const express = require('express')
const path = require('path')
const port = 3000
const app = express()

// serve vue static assets that are localized in the 'dist' folder (after running npm run build)
app.use(express.static('dist'))

// if the static files are requested, serve the desired path
app.get('/static/*', function (request, response) {
    response.sendFile(path.resolve(__dirname, 'dist', request.path));
});

// else serve index.html (this allow the vue router to manage the other urls)
app.get('/*', function (request, response){
    response.sendFile(path.resolve(__dirname, 'dist', 'index.html'));
});

// starting the server
app.listen(port)
console.log('server started on port ' + port)
