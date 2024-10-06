import { useState } from 'react';
import { IoIosArrowDown } from 'react-icons/io';
import './App.css';
import { handleButtonClick, handleInputChange, handleCallClick, handleScrollDown } from './handlers'; // Import the functions

function App() {
  const [pressedButton, setPressedButton] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [errorMessage, setErrorMessage] = useState(''); // State for error message

  return (
    <>
      <div className="centered-header">
        <h1 className="fade-in-on-start">Welcome to <span className="highlight">Overphone</span>!</h1>
        <p className="fade-in-on-start">Overphone is an intelligent AI-powered call agent that responds precisely to your specific needs.</p>
        <IoIosArrowDown className="scroll-icon" onClick={handleScrollDown}/>
      </div>
      <div className="content-backdrop">
        <div className="content">
          <p>Select one of our AI personas to speak to below:</p>
          <div className="button-container">
            <button
              className={`circle-button ${pressedButton === 'Banking' ? 'pressed' : ''}`}
              onClick={() => handleButtonClick('Banking', pressedButton, setPressedButton)}
            >
              Banking
            </button>
            <button
              className={`circle-button ${pressedButton === 'Accelerator' ? 'pressed' : ''}`}
              onClick={() => handleButtonClick('Accelerator', pressedButton, setPressedButton)}
            >
              Accelerator
            </button>
            <button
              className={`circle-button ${pressedButton === 'Mental Health' ? 'pressed' : ''}`}
              onClick={() => handleButtonClick('Mental Health', pressedButton, setPressedButton)}
            >
              Mental Health
            </button>
          </div>
          <div className="text-field-container">
            <input
              type="text"
              className="text-field"
              placeholder="Enter your phone number here"
              value={phoneNumber}
              onChange={(event) => handleInputChange(event, setPhoneNumber)}
            />
            <button className="call-button" onClick={() => handleCallClick(phoneNumber, setErrorMessage)}>Call!</button>
          </div>
          <p className="error">{errorMessage}</p> {/* Display error message */}
        </div>
      </div>
      
    </>
  );
}

export default App;