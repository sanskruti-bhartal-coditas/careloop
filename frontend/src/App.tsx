import { Provider } from "react-redux";
import { store } from "./redux/store/store";
import { RouterProvider } from "react-router-dom";
import { router } from "./router/router";
import { AuthLoader } from "./components/AuthLoader/AuthLoader";
import Patient from "./pages/Patient/Patient";

const App = () => {
  return (
    <Provider store={store}>
      {/* <AuthLoader>
        <RouterProvider router={router} />
      </AuthLoader> */}
        <Patient/>
    </Provider>
  
  );
};

export default App;