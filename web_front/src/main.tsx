import ReactDOM from "react-dom/client";
import { App } from "./App.tsx";
import "./index.css";
import { reatomContext } from "@reatom/npm-react";
import { ctx } from "./model";
import "@mantine/core/styles.css";

import { MantineProvider } from "@mantine/core";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <MantineProvider>
    <reatomContext.Provider value={ctx}>
      <App />
    </reatomContext.Provider>
  </MantineProvider>,
);
