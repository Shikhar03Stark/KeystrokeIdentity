import React, { useState, useEffect, useRef, useCallback } from "react";
import { useLocation } from "react-router-dom";

const KeyStrokeIntake = () => {
  const location = useLocation();
  const userId = location.state?.userId;  // Access the user ID from state
  const [phrases] = useState([
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "I think, therefore I am."
  ]);
  const [currentPhrase, setCurrentPhrase] = useState(phrases[0]);
  const [inputText, setInputText] = useState("");
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/register_keystrokes");

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

  const sendKeyEvent = useCallback((eventType, key) => {
    const timestamp = new Date().getTime();
    const payload = JSON.stringify({
      event_type: eventType, // 'D' for down, 'U' for up
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
  }, [userId]); // Add userId as dependency for sendKeyEvent

  const handleKeyDown = useCallback((e) => {
    sendKeyEvent("D", e.key); // 'D' for key down
  }, [sendKeyEvent]);  // Include sendKeyEvent as dependency

  const handleKeyUp = useCallback((e) => {
    sendKeyEvent("U", e.key); // 'U' for key up
  }, [sendKeyEvent]);  // Include sendKeyEvent as dependency

  const handleChange = (e) => {
    setInputText(e.target.value);

    if (e.target.value === currentPhrase) {
      const nextIndex = phrases.indexOf(currentPhrase) + 1;
      if (nextIndex < phrases.length) {
        setCurrentPhrase(phrases[nextIndex]);
        setInputText("");
      } else {
        alert("You've completed all phrases!");
      }
    }
  };

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, [handleKeyDown, handleKeyUp]);  // Now these functions are dependencies

  return (
    <div>
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
  );
};

export default KeyStrokeIntake;
