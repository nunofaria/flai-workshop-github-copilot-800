import React, { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../api/config';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('Fetching teams from:', API_ENDPOINTS.TEAMS);
    }
    
    fetch(API_ENDPOINTS.TEAMS)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams data received:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Processed teams data:', teamsData);
        setTeams(teamsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2>⚔️ Teams</h2>
      <p className="text-muted">Superhero team competition</p>
      
      <div className="row">
        {teams.map(team => (
          <div key={team._id} className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{team.name}</h5>
                <p className="card-text">
                  <strong>Description:</strong> {team.description}<br />
                  <strong>Total Points:</strong> <span className="badge bg-success">{team.total_points}</span>
                </p>
                <div>
                  <strong>Members:</strong>
                  <ul className="list-group list-group-flush mt-2">
                    {(() => {
                      try {
                        const members = typeof team.members === 'string' 
                          ? JSON.parse(team.members.replace(/'/g, '"'))
                          : Array.isArray(team.members) ? team.members : [];
                        return members.map((member, index) => (
                          <li key={index} className="list-group-item">{member}</li>
                        ));
                      } catch (error) {
                        console.error('Error parsing team members:', error);
                        return <li className="list-group-item text-danger">Error loading members</li>;
                      }
                    })()}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Teams;
