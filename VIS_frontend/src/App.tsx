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
import {TestStatistics} from "./pages/TestStatistics.tsx";
import {AdminDashboard} from "./pages/AdminDashboard.tsx";
import {QuestionStatistics} from "./pages/QuestionStatistics.tsx";

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
                  <Route path="/test-statistics/:id" element={<TestStatistics />} />
                  <Route path="/question_statistics/:id" element={<QuestionStatistics />} />
                  <Route path="/admin_dashboard" element={<AdminDashboard />} />
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
