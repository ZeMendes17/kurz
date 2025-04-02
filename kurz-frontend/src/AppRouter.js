import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import MovieClip from "./MovieClip" 

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/movie/tt0114148" />} />
        <Route path="/movie/:id" element={<MovieClip />} />
        <Route path="*" element={<Navigate to="/movie/tt0114148" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
