import React, { useState } from "react";
import axios from "axios";

function App() {
  const [type, setType] = useState("compute");
  const [size, setSize] = useState(10);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const res = await axios.post("http://localhost:8000/recommend", {
      type,
      size: parseFloat(size)
    });
    setResult(res.data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Hybrid Cloud Cost Optimizer</h2>
      <label>Workload Type:</label>
      <select value={type} onChange={(e) => setType(e.target.value)}>
        <option value="compute">Compute</option>
        <option value="storage">Storage</option>
        <option value="mixed">Mixed</option>
      </select>
      <br /><br />
      <label>Workload Size:</label>
      <input type="number" value={size} onChange={(e) => setSize(e.target.value)} />
      <br /><br />
      <button onClick={handleSubmit}>Estimate</button>

      {result && (
        <div>
          <h3>Recommendation:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
