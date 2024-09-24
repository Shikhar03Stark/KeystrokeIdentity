import React, { useState, useEffect, useRef, useCallback } from "react";
import { useLocation, useNavigate } from "react-router-dom"; // Import useNavigate
import "./KeyStrokeIntake.css"; // Import the CSS file
import config from "../config"

const KeyStrokeIntake = () => {
  const location = useLocation();
  const navigate = useNavigate(); // Hook for navigation
  const userId = location.state?.userId; // Access the user ID from state
  const [phrases] = useState([
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "I think, therefore I am."
  ]);
  const [currentPhrase, setCurrentPhrase] = useState(phrases[0]);
  const [inputText, setInputText] = useState("");
  const [phraseIndex, setPhraseIndex] = useState(0);
  const [countdown, setCountdown] = useState(3); // Timer state for 3-second countdown
  const [showSuccessMessage, setShowSuccessMessage] = useState(false); // Message state
  const ws = useRef(null);
<<<<<<< Updated upstream
=======
  const backend_url = `http://${config.backend_host}` // http://keystroke.devitvish.in
>>>>>>> Stashed changes

  // Initialize WebSocket connection and send INIT event
  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/register_keystrokes");

    ws.current.onopen = () => {
      console.log("WebSocket connection established.");
      // Send INIT message with userId
      const initMessage = {
        mode: "INIT",
        user_id: userId
      };
      ws.current.send(JSON.stringify(initMessage));
    };

    ws.current.onclose = () => {
      console.log("WebSocket connection closed.");
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [userId]);

  // Function to send key event (STROKE mode)
  const sendKeyEvent = useCallback((eventType, key) => {
    const timestamp = new Date().getTime();
    const payload = JSON.stringify({
      event_type: eventType, // 'D' for key down, 'U' for key up
      key: key.charCodeAt(0), // Send key as ASCII code
      timestamp
    });

    const message = {
      mode: "STROKE",
      payload,
      user_id: userId
    };

    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, [userId]);

  // Handle key down event
  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === "Enter" && inputText === currentPhrase) {
        // When phrase is completed and Enter is pressed, send NEXT event
        const nextMessage = {
          mode: "NEXT",
          user_id: userId
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
            user_id: userId
          };
          ws.current.send(JSON.stringify(endMessage));

          // Show success message and start countdown timer
          setShowSuccessMessage(true);

          let timer = 3;
          const countdownInterval = setInterval(() => {
            setCountdown(timer);
            timer--;
            if (timer < 0) {
              clearInterval(countdownInterval);
              navigate("/"); // Redirect to home page after countdown
            }
          }, 1000);
        }
      } else {
        sendKeyEvent("D", e.key); // 'D' for key down
      }
    },
    [inputText, currentPhrase, phraseIndex, userId, phrases, sendKeyEvent, navigate]
  );

  // Handle key up event
  const handleKeyUp = useCallback(
    (e) => {
      sendKeyEvent("U", e.key); // 'U' for key up
    },
    [sendKeyEvent]
  );

  // Handle input change (text entry)
  const handleChange = (e) => {
    setInputText(e.target.value);
  };

  // Add event listeners for key down and key up
  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, [handleKeyDown, handleKeyUp]);

  return (
    <div className="keystroke-container">
      <h3 className="keystroke-title">Type the following phrase:</h3>
      <p className="keystroke-phrase">{currentPhrase}</p>
      <input
        className="keystroke-input"
        type="text"
        value={inputText}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        onKeyUp={handleKeyUp}
        placeholder="Start typing here..."
      />

      {showSuccessMessage && (
        <div className="success-message">
          <h3>Signup successful!</h3>
          <p>Redirecting to home page in {countdown}...</p>
        </div>
      )}
    </div>
  );
};

export default KeyStrokeIntake;
