import { reatomComponent } from "@reatom/npm-react";
import MainPage from "./pages/MainPage";
import SearchPage from "./pages/SearchPage";

import { pathAtom } from "./model";

export const App = reatomComponent(({ ctx }) => {
  // const thePath = ctx.spy(pathAtom);
  const thePath = window.location.pathname; 

  if (thePath === "/search") {
    return <SearchPage />;
  }
  if (thePath === "/") {
    return <MainPage />;
  }
}, "App");
