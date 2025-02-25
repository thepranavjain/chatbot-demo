import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router";
import AllChatsPage from "./components/AllChatsPage";
import HomePage from "./components/HomePage";
import { AuthProvider } from "./context/AuthContext";
import PrivateRoute from "./components/PrivateRoute";
import ChatPage from "./components/ChatPage";

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Router>
          <Routes>
            <Route path="" element={<HomePage />} />
            <Route
              path="/chat"
              element={
                <PrivateRoute>
                  <AllChatsPage />
                </PrivateRoute>
              }
            />
            <Route
              path="/chat/:sessionId"
              element={
                <PrivateRoute>
                  <ChatPage />
                </PrivateRoute>
              }
            />
          </Routes>
        </Router>
      </div>
    </AuthProvider>
  );
}

export default App;
