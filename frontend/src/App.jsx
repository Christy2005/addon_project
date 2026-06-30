import { useState } from "react";
import axios from "axios";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {
  const [file, setFile] = useState(null);
  const [reportText, setReportText] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const BACKEND = process.env.REACT_APP_BACKEND;

  async function uploadPDF() {
    if (!file) {
      alert("Select a PDF first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await axios.post(
        `${BACKEND}/upload-report`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setReportText(res.data.report_text);
      alert("Report Uploaded Successfully!");
    } catch (err) {
      alert("Upload Failed");
    }

    setLoading(false);
  }

  async function askQuestion() {
    if (question === "") {
      alert("Enter a question.");
      return;
    }

    if (reportText === "") {
      alert("Upload a report first.");
      return;
    }

    setLoading(true);

    try {
      const res = await axios.post(`${BACKEND}/chat`, {
        question: question,
        report_text: reportText,
      });

      setAnswer(res.data.answer);
      setSources(res.data.sources);
    } catch (err) {
      alert("Chat Failed");
    }

    setLoading(false);
  }

  return (
    <div className="container">

      <h1>AI Health Report Diet Planner</h1>

      <div className="card">

        <h2>Upload Blood Report</h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={uploadPDF}>
          Upload Report
        </button>

      </div>

      <div className="card">

        <h2>Ask the AI</h2>

        <textarea
          rows="4"
          placeholder="Ask something like 'Explain my report'"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button onClick={askQuestion}>
          Ask
        </button>

      </div>

      {loading && <h3>Processing...</h3>}

      {answer && (

        <div className="card">

          <h2>AI Response</h2>

          <ReactMarkdown>{answer}</ReactMarkdown>
        </div>

      )}

      {sources.length > 0 && (

        <div className="card">

          <h2>Retrieved Sources (RAG)</h2>

          {sources.map((source, index) => (

            <div key={index} className="source">

              {source}

            </div>

          ))}

        </div>

      )}

    </div>
  );
}

export default App;