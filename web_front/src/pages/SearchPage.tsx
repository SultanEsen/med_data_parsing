import { reatomComponent } from "@reatom/npm-react";

import { redirect } from "../model";

const SearchPage = reatomComponent(({ ctx }) => {
  return (
    <div id="app">
      <div className="search-page">
        <div className="search-header">
          <h4>SearchPage</h4>
          <button onClick={() => redirect(ctx, "/")}>Back</button>
          <div className="search-form"></div>
        </div>
      </div>
    </div>
  );
}, "SearchPage");

export default SearchPage;
