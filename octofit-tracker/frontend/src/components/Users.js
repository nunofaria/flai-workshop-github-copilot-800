import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const codespace = process.env.REACT_APP_CODESPACE_NAME || 'localhost:8000';
  const protocol = process.env.REACT_APP_CODESPACE_NAME ? 'https' : 'http';
  const apiUrl = `${protocol}://${codespace}/api/users/`;

  useEffect(() => {
    console.log('Fetching users from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Users data received:', data);
        // Handle both paginated (.results) and plain array responses
        const usersData = data.results || data;
        console.log('Processed users data:', usersData);
        setUsers(usersData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching users:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2>🦸 OctoFit Users</h2>
      <p className="text-muted">Superhero fitness profiles</p>
      
      <div className="row">
        {users.map(user => (
          <div key={user._id} className="col-md-4 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">
                  {user.avatar} {user.name}
                </h5>
                <p className="card-text">
                  <strong>Email:</strong> {user.email}<br />
                  <strong>Team:</strong> {user.team}<br />
                  <strong>Points:</strong> <span className="badge bg-primary">{user.total_points}</span>
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Users;
