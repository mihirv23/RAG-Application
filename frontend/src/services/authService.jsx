import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

// this is the url on which our bckend fastapi is running

export default API;