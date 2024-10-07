import {BrowserRouter, Route, Routes} from "react-router-dom";
import {Index} from "./pages/Index.tsx";
import {NoPage} from "./pages/NoPage.tsx";
import {Tests} from "./pages/Tests.tsx";
import {Test} from "./pages/Test.tsx";
import {NewTest} from "./pages/NewTest.tsx";
import {Header} from "./components/Header.tsx";
import {Profile} from "./pages/Profile.tsx";

function App() {

  return (
      <BrowserRouter>
          <Header />
          <Routes>
              <Route path="/" element={<Index />} />
              <Route path="/tests" element={<Tests />} />
              <Route path="/test/:id" element={<Test />} />
              <Route path="/new_test/:id" element={<NewTest />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="*" element={<NoPage />} />
          </Routes>
      </BrowserRouter>
  )
}

export default App
