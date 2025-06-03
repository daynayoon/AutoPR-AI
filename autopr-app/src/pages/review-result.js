import { useState, useEffect } from "react";
import axios from "axios";

export default function ReviewResult() {
  const [review, setReview] = useState(null);
  const [progress, setProgress] = useState(0);
  const fileId =
    typeof window !== "undefined" ? localStorage.getItem("file_id") : null;

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => (prev < 100 ? prev + 10 : 100));
    }, 300);
    if (fileId) {
      axios
        .post("http://localhost:8000/review/analyze", { file_id: fileId })
        .then((res) => setReview(res.data))
        .catch((err) => console.error(err));
    }
    return () => clearInterval(interval);
  }, []);

  if (!review) {
    return (
      <div style={{ textAlign: "center", marginTop: "20%" }}>
        <h1>Analyzing...</h1>
        <progress value={progress} max="100"></progress>
        <p>{progress}%</p>
      </div>
    );
  }

  return (
    <div style={{ textAlign: "center", marginTop: "20%" }}>
      <h1>Review Result</h1>
      <ul>
        {review.review_comments.map((comment, idx) => (
          <li key={idx}>{comment}</li>
        ))}
      </ul>
      <button onClick={() => (window.location.href = "/create-pr")}>
        Create Pull Request
      </button>
    </div>
  );
}
