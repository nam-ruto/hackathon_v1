import React from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css";
import img3 from "../assets/3.png";
import img5 from "../assets/5.jpg";
import img6 from "../assets/6.jpg";

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="main">
      <div className="nav">
        <div className="nav-part-1">
          <ul>
            <li>Home</li>
            <li>Admissions</li>
            <li>Academics</li>
            <li>Resources</li>
            <li>Contact</li>
          </ul>
        </div>
      </div>
      <div className="content">
        <div className="content-left">
          <h5>Your Troy Assistant</h5>
          <h1>Troy University Chatbot</h1>
          <p>
            Chat now for quick and easy support on academics, student services,
            and more at Troy University!
          </p>
          <button className="btn" onClick={() => navigate("/chat")}>
            Chat Now
          </button>
        </div>
        <div className="content-right">
          <div className="product">
            <img src={img3} alt="troy" />
            <button className="btnss" onClick={() => navigate("/chat")}>
              AI CATALOG
            </button>
          </div>
          <div className="product">
            <img src={img5} alt="troy" />
            <button className="btnss" onClick={() => navigate("/chat")}>
              AI ADVISOR
            </button>
          </div>
          <div className="product">
            <img src={img6} alt="troy" />
            <button className="btnss" onClick={() => navigate("/gpa")}>
              GPA EVALUATE
            </button>
          </div>

          <div className="product">
            <img src={img6} alt="troy" />
            <button className="btnss" onClick={() => navigate("/campus")}>
              Campus Guide
            </button>
          </div>
          <div className="product">
            <img src={img6} alt="troy" />
            <button className="btnss" onClick={() => navigate("/scholarship")}>
              Scholarship Matching
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
