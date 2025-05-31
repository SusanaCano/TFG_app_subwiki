// src/app/components/Button.tsx
'use client'; // Esto permite manejar eventos en el frontend

export default function Button({ onClick, children }: { onClick: () => void; children: React.ReactNode }) {
  return <button onClick={onClick}>{children}</button>;
}
