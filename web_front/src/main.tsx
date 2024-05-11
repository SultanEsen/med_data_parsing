import ReactDOM from "react-dom/client";
import { App } from "./App.tsx";
import "./index.css";
import { reatomContext } from "@reatom/npm-react";
import { ctx } from "./model";


ReactDOM.createRoot(document.getElementById("root")!).render(
    <reatomContext.Provider value={ctx}>
      <App />
    </reatomContext.Provider>,
);
