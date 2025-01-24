import axios from "axios";
import { getIdToken } from "firebase/auth";
import { auth } from "../firebase";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"; // Default fallback

export const axiosInstance = axios.create({
  baseURL: API_URL,
});

export const axiosAuthInstance = axios.create({
  baseURL: API_URL,
});

axiosAuthInstance.interceptors.request.use(
  async (config) => {
    const user = auth.currentUser;
    if (user) {
      try {
        const token = await getIdToken(user); // Fetch the Firebase ID token
        if (config.headers) {
          config.headers["Authorization"] = `Bearer ${token}`;
        }
      } catch (error) {
        console.error("Error getting ID token:", error);
        return Promise.reject(error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
