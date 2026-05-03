import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.js';

// Polyfill Node.js Buffer for axios when bundling with Parcel. Axios uses Buffer
// internally in its form-data helper, and Parcel v2 does not automatically
// polyfill Node builtins. Installing the `buffer` package and assigning
// Buffer to the global scope resolves the build error seen during Vercel
// deployment ("Failed to resolve 'buffer' ...").
import { Buffer } from 'buffer';
// eslint-disable-next-line no-undef
window.Buffer = Buffer;

// Render the App component into the DOM. We use React 18's `createRoot`
const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);