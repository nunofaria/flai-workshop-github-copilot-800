import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const codespace = process.env.REACT_APP_CODESPACE_NAME || 'localhost:8000';
  const protocol = process.env.REACT_APP_CODESPACE_NAME ? 'https' : 'http';
  const apiUrl = `${protocol}://${codespace}/api/workouts/`;

  useEffect(() => {
    console.log('Fetching workouts from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Processed workouts data:', workoutsData);
        setWorkouts(workoutsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      beginner: 'success',
      intermediate: 'warning',
      advanced: 'danger'
    };
    return badges[difficulty] || 'secondary';
  };

  if (loading) return <div className="container mt-4"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2>💪 Workout Recommendations</h2>
      <p className="text-muted">Personalized superhero training programs</p>
      
      <div className="row">
        {workouts.map(workout => (
          <div key={workout._id} className="col-md-6 mb-4">
            <div className="card h-100">
              <div className="card-header">
                <h5 className="card-title mb-0">{workout.name}</h5>
                <span className={`badge bg-${getDifficultyBadge(workout.difficulty)}`}>
                  {workout.difficulty}
                </span>
                <span className="badge bg-info ms-2">{workout.duration} min</span>
              </div>
              <div className="card-body">
                <p className="card-text">{workout.description}</p>
                
                <h6>Target Muscle Groups:</h6>
                <div className="mb-3">
                  {(Array.isArray(workout.target_muscle_groups) 
                    ? workout.target_muscle_groups 
                    : []
                  ).map((group, index) => (
                    <span key={index} className="badge bg-secondary me-1">{group}</span>
                  ))}
                </div>

                <h6>Exercises:</h6>
                <ul className="list-group list-group-flush">
                  {(Array.isArray(workout.exercises) 
                    ? workout.exercises 
                    : []
                  ).map((exercise, index) => (
                    <li key={index} className="list-group-item">
                      <strong>{exercise.name || 'Exercise'}</strong>
                      {exercise.sets && ` - ${exercise.sets} sets`}
                      {exercise.reps && ` × ${exercise.reps} reps`}
                      {exercise.duration && ` - ${exercise.duration}`}
                      {exercise.distance && ` - ${exercise.distance}`}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Workouts;
