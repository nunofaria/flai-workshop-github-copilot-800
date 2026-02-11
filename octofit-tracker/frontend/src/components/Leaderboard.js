import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  // API endpoint: https://miniature-fiesta-wx74x6gjqxqc94rw-8000.app.github.dev/api/leaderboard/
  const codespace = process.env.REACT_APP_CODESPACE_NAME || 'localhost:8000';
  const protocol = process.env.REACT_APP_CODESPACE_NAME ? 'https' : 'http';
  const apiUrl = `${protocol}://${codespace}/api/leaderboard/`;

  useEffect(() => {
    console.log('Fetching leaderboard from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard data received:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Processed leaderboard data:', leaderboardData);
        setLeaderboard(leaderboardData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  const filteredData = filter === 'all' 
    ? leaderboard 
    : leaderboard.filter(entry => entry.type === filter);

  const individualLeaders = filteredData.filter(entry => entry.type === 'individual');
  const teamLeaders = filteredData.filter(entry => entry.type === 'team');

  return (
    <div className="container mt-4">
      <h2>🏆 Leaderboard</h2>
      <p className="text-muted">Top performers and team rankings</p>

      <div className="btn-group mb-3" role="group">
        <button 
          className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-outline-primary'}`}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button 
          className={`btn ${filter === 'individual' ? 'btn-primary' : 'btn-outline-primary'}`}
          onClick={() => setFilter('individual')}
        >
          Individual
        </button>
        <button 
          className={`btn ${filter === 'team' ? 'btn-primary' : 'btn-outline-primary'}`}
          onClick={() => setFilter('team')}
        >
          Teams
        </button>
      </div>

      {(filter === 'all' || filter === 'individual') && individualLeaders.length > 0 && (
        <div className="mb-4">
          <h4>Individual Rankings</h4>
          <div className="table-responsive">
            <table className="table table-striped">
              <thead className="table-dark">
                <tr>
                  <th>Rank</th>
                  <th>Name</th>
                  <th>Team</th>
                  <th>Points</th>
                </tr>
              </thead>
              <tbody>
                {individualLeaders.map(entry => (
                  <tr key={entry._id} className={entry.rank <= 3 ? 'table-warning' : ''}>
                    <td>
                      {entry.rank === 1 && '🥇'}
                      {entry.rank === 2 && '🥈'}
                      {entry.rank === 3 && '🥉'}
                      {entry.rank > 3 && entry.rank}
                    </td>
                    <td><strong>{entry.name}</strong></td>
                    <td>{entry.team}</td>
                    <td><span className="badge bg-primary">{entry.points}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {(filter === 'all' || filter === 'team') && teamLeaders.length > 0 && (
        <div className="mb-4">
          <h4>Team Rankings</h4>
          <div className="table-responsive">
            <table className="table table-striped">
              <thead className="table-dark">
                <tr>
                  <th>Rank</th>
                  <th>Team</th>
                  <th>Points</th>
                </tr>
              </thead>
              <tbody>
                {teamLeaders.map(entry => (
                  <tr key={entry._id} className={entry.rank === 1 ? 'table-success' : 'table-secondary'}>
                    <td>
                      {entry.rank === 1 && '🏆'}
                      {entry.rank === 2 && '🥈'}
                      {entry.rank > 2 && entry.rank}
                    </td>
                    <td><strong>{entry.name}</strong></td>
                    <td><span className="badge bg-success">{entry.points}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default Leaderboard;
