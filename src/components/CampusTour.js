import React, { useState } from 'react';
import './ChatScreen.css';
import userLogo from '../assets/usericon.svg';
import respLogo from '../assets/sendicon.svg';

// Header Component
const Header = () => {
  return (
    <header className="header">
      <h1>🤖 Troy Campus Guide</h1>
      <p>Hi, how can I help you today?</p>
    </header>
  );
};

// MessageBox Component (User's Input)
const MessageBox = ({ message }) => {
  return (
    <div className="message-box user">
      <img className='logo1' src={userLogo} alt="User Logo" />
      <div>{message}</div>
    </div>
  );
};

// AnswerBox Component (AI Response or Loading)
const AnswerBox = ({ message }) => {
  return (
    <div className="message-box ai">
      <img className='logo2' src={respLogo} alt="AI Logo" />
      <div>{message}</div>
    </div>
  );
};

// Footer Component (User Input Field)
const Footer = ({ userInput, setUserInput, handleSend }) => {
  return (
    <footer className="footer">
      <div className="input-container">
        <input
          type="text"
          placeholder="Ask question"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)} // Update the user input state
        />
        {/* <button className="send-button" onClick={handleSend}>
          <i className="fas fa-paper-plane"></i>
        </button> */}

<button className="send-button" onClick={handleSend}>Send
        </button>
      </div>
    </footer>
  );
};

// App Component (Main Layout)
const App = () => {
  const [userInput, setUserInput] = useState(''); // State to track user's input
  const [messages, setMessages] = useState([]);   // State to track conversation


  const handleSend = async () => {
    if (userInput.trim() === '') return; // Don't send empty input
  
    // Add user input to messages
    const newMessage = { sender: 'user', text: userInput };
    setMessages((prevMessages) => [...prevMessages, newMessage]); // Use functional state update
    setUserInput(''); // Clear the input field immediately

    // setMessages((prevMessages) => [...prevMessages, { sender: 'ai', text: 'Typing...' }]);
  
    try {
      const response = await fetch('http://127.0.0.1:8000/campus', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: newMessage.text,
          session_id: Date.now().toString(),
        }),
      });
  
      const data = await response.json();
      console.log("data", data);
  
      const aiMessage = { sender: 'ai', text: data?.answer || data };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
      // setMessages(() => [aiMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage = { sender: 'ai', text: 'Something went wrong. Please try again.' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]); // Append error message to messages
    }
  };
  

  return (
    <div className="app">
      <Header />
      
      {messages.map((msg, index) =>
        msg.sender === 'user' ? (
          <MessageBox key={index} message={msg.text} />
        ) : (
          <AnswerBox key={index} message={msg.text} />
        )
      )}

      <Footer userInput={userInput} setUserInput={setUserInput} handleSend={handleSend} />
    </div>
  );
};

export default App;
