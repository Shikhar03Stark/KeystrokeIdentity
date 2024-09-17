import React, { useState, useEffect, useRef } from "react";

const KeyStrokeIntake = () => {
  const [phrases] = useState([
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "I think, therefore I am."
  ]);

  const [currentPhrase, setCurrentPhrase] = useState(phrases[0]);
  const [inputText, setInputText] = useState("");
  const [keyEvents, setKeyEvents] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/ws");

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

  const handleKeyDown = (e) => {
    const timestamp = new Date().getTime();
    const keyPressed = e.key;
    
    setKeyEvents((prevEvents) => [
      ...prevEvents,
      { key: keyPressed, type: "keydown", timestamp }
    ]);
  };

  const handleKeyUp = (e) => {
    const timestamp = new Date().getTime();
    const keyPressed = e.key;
    
    setKeyEvents((prevEvents) => [
      ...prevEvents,
      { key: keyPressed, type: "keyup", timestamp }
    ]);
  };

  const handleChange = (e) => {
    setInputText(e.target.value);

    if (e.target.value === currentPhrase) {
      const nextIndex = phrases.indexOf(currentPhrase) + 1;
      if (nextIndex < phrases.length) {
        setCurrentPhrase(phrases[nextIndex]);
        setInputText("");
      } else {
        alert("You've completed all phrases!");
        ws.current.send(JSON.stringify(keyEvents));
      }
    }
  };

  useEffect(() => {
    const handleKeyPressAndRelease = () => {
      window.addEventListener("keydown", handleKeyDown);
      window.addEventListener("keyup", handleKeyUp);

      return () => {
        window.removeEventListener("keydown", handleKeyDown);
        window.removeEventListener("keyup", handleKeyUp);
      };
    };

    handleKeyPressAndRelease();
  }, []);

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
