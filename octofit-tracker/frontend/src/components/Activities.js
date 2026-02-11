import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const codespace = process.env.REACT_APP_CODESPACE_NAME || 'localhost:8000';
  const protocol = process.env.REACT_APP_CODESPACE_NAME ? 'https' : 'http';
  const apiUrl = `${protocol}://${codespace}/api/activities/`;

  useEffect(() => {
    console.log('Fetching activities from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities data received:', data);
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Processed activities data:', activitiesData);
        setActivities(activitiesData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching activities:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2>🏃 Fitness Activities</h2>
      <p className="text-muted">Recent superhero workouts and activities</p>
      
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th>User</th>
              <th>Activity</th>
              <th>Duration</th>
              <th>Distance</th>
              <th>Calories</th>
              <th>Points</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {activities.slice(0, 20).map(activity => (
              <tr key={activity._id}>
                <td>{activity.user_name}</td>
                <td>
                  <span className="badge bg-info">{activity.activity_type}</span>
                </td>
                <td>{activity.duration} min</td>
                <td>{activity.distance > 0 ? `${activity.distance} km` : '-'}</td>
                <td>{activity.calories}</td>
                <td><span className="badge bg-primary">{activity.points}</span></td>
                <td>{new Date(activity.date).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Activities;
