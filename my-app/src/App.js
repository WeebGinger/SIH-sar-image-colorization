import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [imageUrl, setImageUrl] = useState(''); // State for uploaded image URL

  // Handle file input change
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Handle file upload
  const handleFileUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('image', selectedFile);

      try {
        const response = await fetch('/upload', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();
        if (response.ok) {
          setUploadStatus(data.msg);
          setImageUrl(`http://localhost:5000/${data.file}`); // Update image URL with server address
        } else {
          setUploadStatus('Upload failed: ' + data.msg);
          setImageUrl(''); // Clear image URL on failure
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        setUploadStatus('Upload failed!');
        setImageUrl(''); // Clear image URL on failure
      }
    } else {
      setUploadStatus('No file selected!');
      setImageUrl(''); // Clear image URL if no file selected
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Upload an Image</h1>

        {/* Image Upload Button */}
        <input
          type="file"
          id="file-upload"
          style={{ display: 'none' }}
          onChange={handleFileChange}
          accept="image/*"
        />
        <label htmlFor="file-upload" className="upload-button">
          Upload Image
        </label>

        {/* Display selected file name */}
        {selectedFile && <p>Selected file: {selectedFile.name}</p>}

        {/* Upload Button */}
        <button onClick={handleFileUpload}>Upload File</button>

        {/* Upload Status */}
        {uploadStatus && <p>{uploadStatus}</p>}

        {/* Display uploaded image if available */}
        {imageUrl && <img src={imageUrl} alt="Uploaded" style={{ marginTop: '20px', maxWidth: '500px' }} />}
      </header>
    </div>
  );
}

export default App;
