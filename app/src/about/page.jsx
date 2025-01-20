/*import './styles.css';

export default function About() {
    return (
      <div style={{ padding: '20px' }}>
        <h1>Acerca de</h1>
        <p>Esta aplicación permite realizar búsquedas en bases de datos biológicas.</p>
      </div>
    );
  }*/
  'use client'

import { useState, useEffect } from "react";

const ApiTest = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Realiza una solicitud al backend
    fetch("http://localhost:8000/api/message")
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setMessage("Error al conectar con el backend.");
      });
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Prueba de comunicación API</h1>
      <p>{message}</p>
    </div>
  );
};

export default ApiTest;
