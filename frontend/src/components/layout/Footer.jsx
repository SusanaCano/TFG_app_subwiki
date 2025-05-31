// src/ app/ components/layout/Footer.jsx
export default function Footer() {
    return (
      <footer style={footerStyle}>
        <p style={textStyle}>© 2025 Mi Aplicación. Todos los derechos reservados.</p>
      </footer>
    );
  }
  
  // Estilos en línea para centrar el contenido y colocarlo al final de la página
  const footerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
   // position: 'absolute',
    position: 'fixed',
    bottom: '0',
    width: '100%',
    backgroundColor: '#333',
    color: '#fff',
    padding: '10px 0',
  };
  
  const textStyle = {
    margin: 0,
    fontSize: '14px',
  };
  