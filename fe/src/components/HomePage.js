import React from 'react';
import './HomePage.css'; // Create and use a separate CSS file for styling

const HomePage = () => {
  // Dummy data to display
  const dummyData = [
    { id: 1, title: "Task 1", description: "Complete the setup of the project" },
    { id: 2, title: "Task 2", description: "Work on user authentication" },
    { id: 3, title: "Task 3", description: "Integrate the WebSocket" },
  ];

  return (
    <div className="home-container">
      <h1>Welcome to the Home Page</h1>
      <p>Here is some dummy data:</p>
      <div className="data-list">
        {dummyData.map((item) => (
          <div key={item.id} className="data-item">
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
