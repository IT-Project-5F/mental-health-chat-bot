import "./App.css";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Map from "./Map.tsx";
import Listing from "./Listing.tsx";
import Login from "./Login.tsx";
import Register from "./Register.tsx";
import ChatContainer from "./chat/ChatContainer.tsx";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>} />
        <Route
          path="/"
          element={
            <div className="w-screen flex overflow-hidden">
              <div className="absolute inset-0">
                <Map/>
              </div>
              <div className="absolute inset-0 top-0 left-0 sm:top-10 sm:left-10">
                <Listing/>
              </div>
              <div className="absolute inset-0 left-0 sm:left-1/2 top-1/2 sm:top-0">
                <ChatContainer/>
              </div>
            </div>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
