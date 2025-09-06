import "./App.css";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Map from "./Map.tsx";
import Listing from "./Listing.tsx";
//import Login from "./Login.tsx";

function App() {

  return (
    <Router>
      <Routes>
        {/*<Route path="/login" element={<Login/>}/>
        */}
        <Route
          path="/"
          element={
            <div className="w-screen h-screen">
              <div className="absolute inset-0">
                <Map/>
              </div>
              <div className="absolute inset-0">
                <Listing/>
              </div>
            </div>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
