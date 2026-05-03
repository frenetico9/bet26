import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.js';

// Render the App component into the DOM. We use React 18's `createRoot`
const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);