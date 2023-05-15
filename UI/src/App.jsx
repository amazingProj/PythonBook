import { useState } from "react";
import Header from "./components/Header/Header";
import "./App.css";

function App() {
  const [user, setUser] = useState(true);

  return (
    <>
      {!user ? (
        <div>Login</div>
      ) : (
        <div>
          <Header />
        </div>
      )}
    </>
  );
}

export default App;
