import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer"; // ⬅️ add this
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Albums from "./pages/Albums";
import SearchResults from "./pages/SearchResults";
import Upload from "./pages/Upload";
import { AuthProvider, useAuthCtx } from "./context/AuthContext";

function Protected({ children }) {
  const { user, ready } = useAuthCtx();
  const loc = useLocation();
  if (!ready) return null;
  if (!user) return <Navigate to="/login" replace state={{ from: loc }} />;
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        {/* App layout */}
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/upload" element={<Protected><Upload /></Protected>} />
              <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
              <Route path="/albums" element={<Protected><Albums /></Protected>} />
              <Route path="/search" element={<Protected><SearchResults /></Protected>} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          <Footer /> 
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}
