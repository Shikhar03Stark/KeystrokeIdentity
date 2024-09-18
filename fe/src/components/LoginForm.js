import React, { useState, useEffect, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginForm.css";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [inputText, setInputText] = useState("");
  const [phrases] = useState([
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "I think, therefore I am."
  ]);
  const [currentPhrase, setCurrentPhrase] = useState(phrases[0]);
  const [phraseIndex, setPhraseIndex] = useState(0);
  const [isTyping, setIsTyping] = useState(false); // State to track typing start
  const [error, setError] = useState(null);
  const ws = useRef(null);
  const navigate = useNavigate();

  // WebSocket connection setup
  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/login_keystrokes");

    ws.current.onopen = () => {
      console.log("WebSocket connection established.");
    };

    ws.current.onclose = () => {
      console.log("WebSocket connection closed.");
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  // Function to send keystroke events
  const sendKeyEvent = useCallback((eventType, key) => {
    const timestamp = new Date().getTime();
    const payload = JSON.stringify({
      event_type: eventType,
      key: key.charCodeAt(0), // Send key as ASCII code
      timestamp,
    });

    const message = {
      mode: "STROKE",
      payload,
      username,
    };

    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, [username]);

  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === "Enter" && inputText === currentPhrase) {
        // When phrase is completed and Enter is pressed, send NEXT event
        const nextMessage = {
          mode: "NEXT",
          username,
        };
        ws.current.send(JSON.stringify(nextMessage));

        // Move to the next phrase if available
        const nextIndex = phraseIndex + 1;
        if (nextIndex < phrases.length) {
          setCurrentPhrase(phrases[nextIndex]);
          setInputText("");
          setPhraseIndex(nextIndex);
        } else {
          // If all phrases are done, send END event
          const endMessage = {
            mode: "END",
            username,
          };
          ws.current.send(JSON.stringify(endMessage));
          alert("You've completed all phrases!");

          // Receive the backend validation response
          ws.current.onmessage = (event) => {
            const response = JSON.parse(event.data);
            if (response.status === "success") {
              navigate("/home"); // Redirect to home on success
            } else {
              setError("Login failed. User authentication did not match.");
            }
          };
        }
      } else {
        sendKeyEvent("D", e.key); // 'D' for key down
      }
    },
    [inputText, currentPhrase, phraseIndex, username, phrases, sendKeyEvent, navigate]
  );

  const handleKeyUp = useCallback(
    (e) => {
      sendKeyEvent("U", e.key); // 'U' for key up
    },
    [sendKeyEvent]
  );

  // Handle input change
  const handleChange = (e) => {
    setInputText(e.target.value);
  };

  const handleUsernameSubmit = (e) => {
    e.preventDefault();
    if (username) {
      setIsTyping(true); // Start the phrase input process
    } else {
      setError("Username is required.");
    }
  };

  // Add key event listeners
  useEffect(() => {
    if (isTyping) {
      window.addEventListener("keydown", handleKeyDown);
      window.addEventListener("keyup", handleKeyUp);
    }

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, [handleKeyDown, handleKeyUp, isTyping]);

  return (
    <div className="LoginForm">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}

      {!isTyping ? (
        <form onSubmit={handleUsernameSubmit}>
          <div>
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <button type="submit">Submit</button>
        </form>
      ) : (
        <div className="phrase-input">
          <h3>Type the following phrase:</h3>
          <p>{currentPhrase}</p>
          <input
            type="text"
            value={inputText}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            onKeyUp={handleKeyUp}
          />
        </div>
      )}
    </div>
  );
};

export default LoginForm;
