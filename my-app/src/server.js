const express = require('express');
const multer = require('multer');
const path = require('path');
const cors = require('cors'); // Enable CORS

const app = express();

// Enable CORS for the frontend on port 3000
app.use(cors({ origin: 'http://localhost:3000' }));

// Serve static files from the 'user-images' directory
app.use('/user-images', express.static(path.join(__dirname, 'user-images')));

// Set storage engine for multer
const storage = multer.diskStorage({
  destination: path.join(__dirname, 'user-images'), // Save to src/user-image folder
  filename: function (req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname)); // Rename file with timestamp
  }
});

// Initialize multer upload
const upload = multer({
  storage: storage,
  limits: { fileSize: 1000000 }, // Limit file size to 1MB
  fileFilter: function (req, file, cb) {
    checkFileType(file, cb);
  }
}).single('image');

// Check File Type function (optional image validation)
function checkFileType(file, cb) {
  const filetypes = /jpeg|jpg|png|gif/;
  const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
  const mimetype = filetypes.test(file.mimetype);

  if (mimetype && extname) {
    return cb(null, true);
  } else {
    cb('Error: Images Only!');
  }
}

// Upload endpoint
app.post('/upload', (req, res) => {
  console.log('File upload request received');
  upload(req, res, (err) => {
    if (err) {
      console.log('Error during file upload:', err);
      res.status(400).send({ msg: err });
    } else {
      if (req.file == undefined) {
        console.log('No file selected!');
        res.status(400).send({ msg: 'No file selected!' });
      } else {
        console.log('File uploaded successfully:', req.file);
        res.status(200).send({
          msg: 'File uploaded successfully!',
          file: `user-images/${req.file.filename}`
        });
      }
    }
  });
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
