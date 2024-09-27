import React from 'react';
import Ranking from './components/Ranking';  // Importing the Ranking component

function App() {
  return (
    <div className="App">
      <h1>LLM Benchmark Rankings</h1>
      <Ranking />  {/* Displaying the Ranking component */}
    </div>
  );
}

export default App;
