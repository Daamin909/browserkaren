import React, { useState, useEffect, useRef } from "react";
import "./App.css";
import NavBar from "./Components/NavBar/NavBar";
import ChatBox from "./Components/ChatBox/ChatBox";
import InputBox from "./Components/InputBox/InputBox";
import { showErrorMessage } from "./Scripts/speechToText";
import client from "./Utils/apiClient";

const App = () => {
  const [messages, setMessages] = useState([]);
  const scrollRef = useRef(null);
  useEffect(() => {
    try {
      client.post("/api/fetch-messages").then((resp) => {
        setMessages(resp.data);
      });
    } catch (err) {
      showErrorMessage(`404: ${err}`);
    }
  }, []);
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);
  return (
    <div className="app">
      <NavBar />
      <div className="chat-interface-container">
        <ChatBox messages={messages} scrollRef={scrollRef} />
        <InputBox messages={messages} setMessages={setMessages} />
      </div>
    </div>
  );
};

export default App;
