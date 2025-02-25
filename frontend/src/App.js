import React, { useState } from 'react';
import './App.css';

function App() {
  const [description, setDescription] = useState('');
  const [image, setImage] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setImage(null);

    try {
      console.log("Sending request to backend with description:", description);

      // Send request to Flask proxy
      const response = await fetch(`http://localhost:8080/search?description=${encodeURIComponent(description)}`);
      console.log("Received response from backend:", response);

      if (response.ok) {
        const data = await response.json();
        console.log("Received image data from backend:", data);
        
        if (data.image) {
          console.log("Image Base64 data:", data.image);
          setImage(data.image);
        } else {
          console.error("No image data found in response:", data);
          setError('No image found.');
        }
      } else {
        console.error("Error response from backend:", response.status, response.statusText);
        setError('No image found.');
      }
    } catch (err) {
      console.error("Error fetching image:", err);
      setError('Error fetching image. Please try again.');
    }
  };

  return (
    <div className="App">
      <h1>Image Search</h1>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Enter image description" 
          value={description} 
          onChange={(e) => setDescription(e.target.value)} 
          required
        />
        <button type="submit">Search</button>
      </form>

      {error && <p className="error">{error}</p>}
      {image && (
        <img 
          key={Date.now()}  // Force React to re-render the image
          src={`data:image/jpeg;base64,${image}`} 
          alt="Search result" 
          style={{ maxWidth: '100%', borderRadius: '10px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)' }}
        />
      )}
    </div>
  );
}

export default App;
