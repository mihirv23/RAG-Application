import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/authService";

export default function Dashboard() {
    const navigate = useNavigate();
    const [documents, setDocuments] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);

    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);

    const [selectedDocument, setSelectedDocument] = useState(null);

    const handleQuery = async () => {

        if (!question.trim()) {
            return;
        }

        try {
            alert("Request in process.Click ok to continue. Response awaiting....");

            const response =
                await API.post(
                    "/query",
                    null,
                    {
                        params: {
                            question, document_id: selectedDocument?.document_id
                        }
                    }
                );

            setMessages((prev) => [
                ...prev,
                {
                    role: "user",
                    text: question
                },
                {
                    role: "assistant",
                    text:
                        response.data.answer
                }
            ]);

            setQuestion("");

        } catch (err) {

            console.error(err);

        }
    };

    const fetchDocuments = async () => {

        try {
            const token =
                localStorage.getItem("token");

            const response =
                await API.get("/documents", {
                    headers: {
                        Authorization:
                            `Bearer ${token}`
                    }
                });

            setDocuments(
                response.data
            );

        } catch (err) {

            console.error(err);

        }
    };
    const handleUpload = async () => {

        if (!selectedFile) {
            alert("Select a PDF first");
            return;
        }

        try {

            const token =
                localStorage.getItem("token");

            const formData =
                new FormData();

            formData.append(
                "file",
                selectedFile
            );

            const response =
                await API.post(
                    "/upload",
                    formData,
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`,
                        },
                    }
                );

            console.log(
                response.data
            );

            fetchDocuments();

        } catch (err) {

            console.error(err);

        }
    };

    useEffect(() => {

        const token =
            localStorage.getItem("token");

        if (!token) {
            navigate("/login");
            return; //check why we wrote this
        }
        fetchDocuments();

    }, []);
    //this use effect is to ensure that dashboard cant be accessed directly without loggin inn



    return (
        <div className="dashboard">

            <div className="left-panel">
                <h2>Documents</h2>
                <div className="upload-section">

                    <label
                        htmlFor="pdf-upload"
                        className="upload-box"
                    >
                        {selectedFile
                            ? selectedFile.name
                            : "📄 Select PDF"}
                    </label>

                    <input
                        id="pdf-upload"
                        type="file"
                        hidden
                        accept=".pdf"
                        onChange={(e) =>
                            setSelectedFile(
                                e.target.files[0]
                            )
                        }
                    />


                    <button
                        onClick={handleUpload}
                    >
                        Upload PDF
                    </button>
                </div>

                <div className="document-list">

                    {documents.length === 0 ? (
                        <p>No documents uploaded</p>
                    ) : (
                        documents.map((doc) => (
                            <div
                                key={doc.document_id}
                                onClick={() =>
                                    setSelectedDocument(doc)
                                }
                                className={
                                    selectedDocument?.document_id ===
                                        doc.document_id
                                        ? "selected-doc"
                                        : "doc-item"
                                }
                            >
                                {doc.filename}
                            </div>
                        ))
                    )}

                </div>

                <button
                    onClick={() => {

                        localStorage.removeItem("token");

                        navigate("/login");

                    }}
                >
                    Logout
                </button>
            </div>

            <div className="right-panel">

                <div className="chat-header">
                    RAG Assistant
                </div>

                <div className="chat-body">

                    {messages.length === 0 ? (

                        <p>
                            Ask a question
                        </p>

                    ) : (

                        messages.map(
                            (msg, index) => (

                                <div
                                    key={index}
                                >
                                    <strong>
                                        {
                                            msg.role ===
                                                "user"
                                                ? "You"
                                                : "AI"
                                        }
                                        :
                                    </strong>

                                    {" "}

                                    {msg.text}
                                </div>
                            )
                        )
                    )}

                </div>

                <div className="chat-input">

                    <input
                        type="text"
                        placeholder="Ask a question..."
                        value={question}
                        onChange={(e) =>
                            setQuestion(
                                e.target.value
                            )
                        }
                    />

                    <button
                        onClick={handleQuery}
                    >
                        Send
                    </button>

                </div>

            </div>

        </div>
    );
}