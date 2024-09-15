import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  // Handle file input change
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    console.log(event.target.files[0]);
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
      </header>
    </div>
  );
}

export default App;
