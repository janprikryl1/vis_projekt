import {BrowserRouter, Route, Routes} from "react-router-dom";
import {Index} from "./pages/Index.tsx";
import {NoPage} from "./pages/NoPage.tsx";
import {Tests} from "./pages/Tests.tsx";
import {Test} from "./pages/Test.tsx";
import {NewTest} from "./pages/NewTest.tsx";
import {Header} from "./components/Header.tsx";
import {Profile} from "./pages/Profile.tsx";
import {ProviderUser} from "./utils/providers/UserProvider.tsx";
import {SignIn} from "./pages/SignIn.tsx";
import {Register} from "./pages/Register.tsx";

function App() {

  return (
      <BrowserRouter>
          <ProviderUser>
              <Header />
              <Routes>
                  <Route path="/" element={<Index />} />
                  <Route path="/tests" element={<Tests />} />
                  <Route path="/test/:id" element={<Test />} />
                  <Route path="/new_test" element={<NewTest />} />
                  <Route path="/new_test/:id" element={<NewTest />} />
                  <Route path="/question/:id" element={<p>Question</p>} />
                  <Route path="/new_question" element={<p>New quesion</p>} />
                  <Route path="/login" element={<SignIn />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="*" element={<NoPage />} />
              </Routes>
          </ProviderUser>
      </BrowserRouter>
  )
}

export default App
