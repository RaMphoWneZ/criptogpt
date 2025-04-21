import React, { useState } from "react";
import axios from "axios";

function App() {
  const [command, setCommand] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8001/command", { command });
      setResponse(res.data.response);
    } catch (error) {
      setResponse("Error al procesar el comando.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-4">TraderGPT</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-md">
        <input
          type="text"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          placeholder="Escribe un comando (ej. !precio BTC)"
          className="w-full p-2 mb-4 rounded bg-gray-800 text-white placeholder-gray-500"
        />
        <button
          type="submit"
          className="w-full p-2 bg-blue-600 rounded hover:bg-blue-700 transition"
        >
          Enviar
        </button>
      </form>
      <div className="mt-4 w-full max-w-md bg-gray-800 p-4 rounded">
        <h2 className="text-xl font-bold mb-2">Respuesta:</h2>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;