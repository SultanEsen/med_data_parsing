import { reatomComponent } from "@reatom/npm-react";

import { columnsAtom } from "../model";

const SearchForm = reatomComponent(({ ctx, setShowModal }) => {
  return (
    <div className="search-dialog">
      {ctx
        .spy(columnsAtom)
        ?.map((column, idx) => (
          <input key={idx} type="text" placeholder={column.replace(/_/g, " ")} />
        ))}
      <button>Search</button>
      <button onClick={() => setShowModal(false)}>Close</button>
    </div>
  );
}, "SearchForm");

export default SearchForm;
