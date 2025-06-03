import { useState } from "react";
import axios from "axios";

export default function CreatePR() {
  const [fileId, setFileId] = useState(localStorage.getItem("file_id"));
  const [repo, setRepo] = useState("");
  const [branch, setBranch] = useState("");
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [token, setToken] = useState("");
  const [result, setResult] = useState(null);
  //   const token = localStorage.getItem("jwt_token");

  const handleCreatePR = async () => {
    try {
      const res = await axios.post(
        "http://localhost:8000/github/pr",
        {
          repo,
          branch,
          title,
          body,
          file_id: fileId,
        },
        {
          headers: { Autjorization: "Bearer ${token}" },
        }
      );
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("PR creation failed :(");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20%" }}>
      <h1>Create PR</h1>
      <input placeholder="Repo" onChange={(e) => setRepo(e.target.value)} />
      <br />
      <input placeholder="Branch" onChange={(e) => setBranch(e.target.value)} />
      <br />
      <input placeholder="Title" onChange={(e) => setTitle(e.target.value)} />
      <br />
      <input placeholder="Body" onChange={(e) => setBody(e.target.value)} />
      <br />
      <button onClick={handleCreatePR}>Create PR</button>
      {result && (
        <p>
          PR #{result.pr_numer}:{" "}
          <a href={result.url} target="_blank">
            {result.url}
          </a>
        </p>
      )}
    </div>
  );
}
