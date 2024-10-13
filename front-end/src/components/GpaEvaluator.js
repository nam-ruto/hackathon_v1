import React, { useState } from 'react';
import './GpaEvaluator.css';

const GpaEvaluator = () => {
  const [courses, setCourses] = useState([
    { courseName: '', credit: '', grade: '' },
  ]);
  const [gpa, setGpa] = useState(null);
  const [apiResponse, setApiResponse] = useState(null);

  const handleCourseChange = (index, event) => {
    const updatedCourses = [...courses];
    updatedCourses[index][event.target.name] = event.target.value;
    setCourses(updatedCourses);
  };

  const handleAddCourse = () => {
    setCourses([...courses, { courseName: '', credit: '', grade: '' }]);
  };

  const handleRemoveCourse = (index) => {
    const updatedCourses = courses.filter((_, i) => i !== index);
    setCourses(updatedCourses);
  };

  const handleCalculateGPA = async () => {
    let totalCredits = 0;
    let totalPoints = 0;

    const gpaInput = {
      "courses": []
    };

    courses.forEach(course => {
      const credit = parseFloat(course.credit);
      const grade = course.grade;
      if (credit && grade) {
        totalCredits += credit;
        totalPoints += grade * credit;
      }
      gpaInput.courses.push({
        "course_name": course.courseName,
        "credit": course.credit,
        "grade": course.grade 
      });
    });

    if (totalCredits > 0) {
      setGpa((totalPoints / totalCredits).toFixed(2));
    } else {
      setGpa(null);
    }

    console.log("gpaInput", JSON.stringify(gpaInput));

    try {
      const response = await fetch('http://127.0.0.1:8000/request-advise', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gpaInput),
      });

      const data = await response.json();
      console.log("gpa resp", data);
      setApiResponse(data); // Store the API response in state

    } catch (error) {
      console.error("Error:", error);
      setApiResponse({ error: 'An error occurred while fetching the response.' });
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">GPA Evaluator</h1>

        <div className="input-container">
          {courses.map((course, index) => (
            <div key={index} className="course-item">
              <input
                type="text"
                name="courseName"
                placeholder="Course Name"
                value={course.courseName}
                onChange={(e) => handleCourseChange(index, e)}
                className="input-field"
              />
              <input
                type="number"
                name="credit"
                placeholder="Credits"
                value={course.credit}
                onChange={(e) => handleCourseChange(index, e)}
                className="input-field"
              />
              <input
                type="text"
                name="grade"
                placeholder="Grade"
                value={course.grade}
                onChange={(e) => handleCourseChange(index, e)}
                className="input-field"
              />
              <button onClick={() => handleRemoveCourse(index)} className="button button-remove">Remove</button>
            </div>
          ))}
        </div>

        <div className="button-group">
          <button onClick={handleAddCourse} className="button">Add Course</button>
          <button onClick={handleCalculateGPA} className="button">Calculate GPA</button>
        </div>

        {gpa !== null && (
          <div className="gpa-result">
            <h2>Calculated GPA: {gpa}</h2>
          </div>
        )}

        {apiResponse && (
          <div className="api-response">
            <h3>Feedback:</h3>
            <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default GpaEvaluator;
