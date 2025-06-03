import { useState } from "react";
import axios from "axios";

export default function upload() {
  const [file, setFile] = useState(null);
  const [fileId, setFileId] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://localhost:8000/review/upload",
        formData
      );
      const fileId = res.data.file_id;
      localStorage.setItem("file_id", fileId);
      alert("Upload successful! :)");
      window.location.href = "/review-result";
    } catch (err) {
      console.error(err);
      alert("Upload failed :(");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20%" }}>
      <h1>AutoPR-AI</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      {fileId && <p>File ID: {fileId}</p>}
    </div>
  );
}
