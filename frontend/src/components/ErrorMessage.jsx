// src/ app/ components/ErrorMessage.jsx

'use client'

import React from 'react';

const ErrorMessage = ({ message }) => {
  return <p style={{ color: 'red' }}>{message}</p>;
};

export default ErrorMessage;
