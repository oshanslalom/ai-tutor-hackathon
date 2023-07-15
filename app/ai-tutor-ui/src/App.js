import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const messageContainerRef = useRef(null);
  const [quizMode, setQuizMode] = useState(false);
  const [quizQuestion, setQuizQuestion] = useState('');
  const [quizOptions, setQuizOptions] = useState([]);

  const startQuiz = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/chatbot', {message: "quiz"}); // Replace with your quiz API endpoint
      const quizData = response.data;

      if (!quizData || !quizData.question || !quizData.options) {
        console.error('Invalid quiz data');
        return;
      }

      setQuizMode(true);
      setQuizQuestion(quizData.question);
      setQuizOptions(quizData.options);
      setMessages([...messages, { text: 'Quiz mode activated!', sender: 'bot' }]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleQuizAnswer = async (selectedAnswer) => {
      const userMessage = `I choose ${selectedAnswer}`;
      addUserMessage(userMessage);

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/chatbot', { message: "QuizAnswer:"+userMessage });
        const botReply = response.data;
        addBotMessage(botReply);
      } catch (error) {
        console.error('Error:', error);
      }

    setQuizMode(false);
  };

  const addUserMessage = (text) => {
    const newMessage = {
      text: text,
      sender: 'user',
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);;
  };

  const addBotMessage = (text) => {
    const newMessage = {
      text: text,
      sender: 'bot',
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);;
  };

  const sendMessage = async() => {
    if (inputText.trim() === '') return;

    if (quizMode) {
      handleQuizAnswer(inputText);
    } else {
      addUserMessage(inputText);

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/chatbot', { message: inputText });
        const botReply = response.data;
        addBotMessage(botReply);
      } catch (error) {
        console.error('Error:', error);
      }
    }

    setInputText('');
  };

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  useEffect(() => {
    messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
  }, [messages]);

  return (
    <div className="App">
      <div className="chat-container">
        <h1 className="title">Kids Chatbot</h1>
        <div className="message-container" ref={messageContainerRef}>
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === 'bot' ? 'bot' : 'user'}`}
            >
              {message.text}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={inputText}
            onChange={handleInputChange}
            placeholder="Type your message..."
          />
          <button onClick={sendMessage}>Send</button>
          {!quizMode && (
            <button onClick={startQuiz}>Start Quiz</button>
          )}
        </div>
        {quizMode && (
          <div className="quiz-container">
            <div className="quiz-question">{quizQuestion}</div>
            <div className="quiz-options">
              {quizOptions.map((option, index) => (
                <div
                  key={index}
                  className="quiz-option"
                  onClick={() => handleQuizAnswer(option)}
                >
                  {option}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
