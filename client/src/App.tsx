import "./App.css";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Map from "./Map.tsx";
// import Listing from "./dropdown/Listing.tsx";
import Login from "./Login.tsx";
import Register from "./Register.tsx";
import ChatContainer from "./chat/ChatContainer.tsx";
import ProtectedRoute from "./ProtectedRoute.tsx";
import Portal from "./admin/Portal.tsx"
import QuickClose from "./QuickClose.tsx";
import ServiceCreationForm from "./formComponents/ServiceCreationForm.tsx";
import { MapProvider } from "./MapContext.tsx";

function App() {

  //const {user} = useAuth();

  return (
    <MapProvider>
      <Router>
      <Routes>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>} />
        <Route
          path="/admin/*"
          element={
              <ProtectedRoute>
                  <Portal />
              </ProtectedRoute>
          }
        />
        {/* TEMP - SERVICE CREATION FORM */}
        <Route path="/service-creation" element={<ServiceCreationForm />} />
        {/* <Route
          path="/admin"
          element={
            <div className="bg-black">
              <Portal/>
            </div>
          }
        /> */}
        <Route
          path="/"
          element={
            <div className="w-screen flex overflow-hidden">
              <div className="z-50 fixed top-0 left-0 w-full group justify-center hidden sm:block">
                <div className="flex justify-end px-20 py-2 bg-[#DCEAAB] opacity-0 -translate-y-full transition-all duration-150 ease-in-out pointer-events-none group-hover:opacity-100 group-hover:translate-y-0 group-hover:pointer-events-auto">
                  <QuickClose/>
                </div>
              </div>
              <div className="absolute z-50 top-3 right-5 block sm:hidden">
                <QuickClose/>
              </div>
              <div className="absolute inset-0">
                <Map/>
              </div>
              {/* <div className="absolute inset-0 top-0 left-0 sm:top-10 sm:left-10">
                <Listing/>
              </div> */}
              <div className="absolute inset-0 left-0 sm:left-1/2 top-1/2 sm:top-0">
                <ChatContainer/>
              </div>
            </div>
          }
        />
      </Routes>
    </Router>
    </MapProvider>
  );
}

export default App;
