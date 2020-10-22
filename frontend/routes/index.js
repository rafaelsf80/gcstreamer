const storage = require('@google-cloud/storage');
const config = require('../local.json');
const storageClient = storage({projectId: config.cloud_project_id, keyfileName: './keyfile.json'});

var express = require('express');
var router = express.Router();

let fileArray = [];

/* GET home page. */
router.get('/', function(req, res, next) {

  const storageBucket = storageClient.bucket(config.video_bucket);
  console.log("Getting files from ", config.video_bucket)
  storageBucket.getFiles(function(err, files) {
    if (!err) {
      files.forEach(function(file) {
        console.log(file.metadata.name.substring(file.metadata.name.indexOf('/')+1, file.metadata.name.length))
        // Show only .mp4 extension videos
        if (String(file.metadata.name).endsWith(".mp4")) {
          fileArray.push({
            device: file.metadata.name.substring(0, file.metadata.name.indexOf('/')),
            video_filename: file.metadata.name.substring(file.metadata.name.indexOf('/')+1, file.metadata.name.length),
            link: file.metadata.mediaLink,
            //url_safe_id: (file.metadata.name).replace('/', '-').replace('.','-'),
            //annotations: body.annotation_results[0],
            //thumbnail: `https://storage.googleapis.com/${config.thumbnail_bucket}/${baseFileName}.png`,
            //preview: `https://storage.googleapis.com/${config.thumbnail_bucket}/${baseFileName}-preview.png`
          });
      }


        // RETURN PAYLOAD
        //if (fileArray.length == files.length) {
        //  res.send(fileArray);
        //}
        
      })  
      //fileArray.forEach(function(item) {
      //  console.log(item.name);
      //});
      
    }
  });

  res.render('index', 
            { title: 'Lista completa de videos', message: 'Hola', 
            estilos: {color: 'red', background: 'indigo'},
            clases: fileArray});

  // Avoid duplication during rendering
  if(fileArray!=null) {
    fileArray = []
  }

//            clases: [fileArray, 'metadata', 'codec']});
});


  

module.exports = router;
