import "./App.css";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from "./Home.tsx";
import Login from "./Login.tsx";
import Register from "./Register.tsx";
import ProtectedRoute from "./ProtectedRoute.tsx";
import Portal from "./admin/Portal.tsx"
import ServiceCreationForm from "./formComponents/ServiceCreationForm.tsx";
import { MapProvider } from "./MapContext.tsx";

function App() {

  return (
    <MapProvider>
      <Router>
        <Routes>
          <Route
            path="/login"
            element={
              <Login/>
            }
          />
          <Route
            path="/register"
            element={
              <Register/>
            }
          />
          <Route
            path="/admin/*"
            element={
                <ProtectedRoute>
                    <Portal />
                </ProtectedRoute>
            }
          />
          <Route
            path="/service-creation"
            element={
              <ServiceCreationForm />
            }
          />
          <Route
            path="/"
            element={
              <Home />
            }
          />
        </Routes>
      </Router>
    </MapProvider>
  );
}

export default App;
