import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import WordDetails from './components/WordDetails';
import './App.css';

function App() {
  const [wordData, setWordData] = useState(null);
  const [error, setError] = useState('');

  const handleSearch = async (word) => {
    try {
      const response = await fetch(`http://localhost:5000/api/search/${word}`);
      if (response.ok) {
        const data = await response.json();
        setWordData(data);
        setError('');
      } else {
        setError('Word not found');
        setWordData(null);
      }
    } catch (err) {
      setError('Error fetching data');
      setWordData(null);
    }
  };

  return (
    <div className="App">
      <h1>The Delight Dictionary</h1>
      <SearchBar onSearch={handleSearch} />
      {error && <p className="error">{error}</p>}
      {wordData && <WordDetails data={wordData} />}
    </div>
  );
}

export default App;
