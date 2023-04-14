import "react-toastify/dist/ReactToastify.css";

import HomePage from "./pages/HomePage";

import { createTheme, ThemeProvider } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";
import { ToastContainer } from "react-toastify";

function App() {
    const theme = createTheme({
        palette: { mode: "dark" }
    });

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <ToastContainer
                position="bottom-left"
                autoClose={4000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnHover
            />
            <HomePage />
        </ThemeProvider>
    );
}

export default App;