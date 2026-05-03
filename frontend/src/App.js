import React, { useEffect, useState } from 'react';
import { fetchSuggestions } from './api.js';

/**
 * Main application component.
 *
 * This component displays a date picker and a list of recommended multi‑bet
 * selections for that date. It calls the backend API to retrieve the
 * suggestions and displays them in a table. Users can adjust the date and
 * refresh the suggestions on demand.
 */
export default function App() {
  const [date, setDate] = useState(() => {
    // Initialise the date input with today in ISO format
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
  });
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch suggestions when the component mounts and whenever the date changes
  useEffect(() => {
    async function loadSuggestions() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchSuggestions(date, 10);
        setSuggestions(data.suggestions);
      } catch (err) {
        setError(err.message || 'Erro ao buscar sugestões');
      } finally {
        setLoading(false);
      }
    }
    loadSuggestions();
  }, [date]);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', margin: '2rem' }}>
      <h1>Previsões de Múltiplas – Futebol</h1>
      <p>
        Escolha uma data para obter recomendações de apostas múltiplas (ambas
        marcam + mais de 2,5 gols) com altas probabilidades.
      </p>
      <label style={{ marginRight: '0.5rem' }}>
        Data:
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          style={{ marginLeft: '0.5rem' }}
        />
      </label>
      {loading && <p>Carregando sugestões…</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && !error && suggestions.length > 0 && (
        <table
          style={{
            width: '100%',
            borderCollapse: 'collapse',
            marginTop: '1rem',
          }}
        >
          <thead>
            <tr>
              <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc' }}>Partida</th>
              <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc' }}>Liga</th>
              <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc' }}>Horário</th>
              <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc' }}>Probabilidade</th>
              <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc' }}>Sugestão</th>
            </tr>
          </thead>
          <tbody>
            {suggestions.map((item, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid #eee' }}>
                <td>
                  {item.home_team} x {item.away_team}
                </td>
                <td>{item.league}</td>
                <td>{new Date(item.match_time).toLocaleString()}</td>
                <td>{(item.probability_bt_and_over25 * 100).toFixed(1)}%</td>
                <td>{item.suggestion}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {!loading && !error && suggestions.length === 0 && (
        <p>Nenhuma partida encontrada para esta data.</p>
      )}
    </div>
  );
}