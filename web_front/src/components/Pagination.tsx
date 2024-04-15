import { reatomComponent } from "@reatom/npm-react";

import { pageAtom, paginationAtom, countryAtom, updatePage } from "../model";

const Pagination = reatomComponent(({ ctx }) => {
  return (
    <div>
      <ul id="pagination">
        {ctx.spy(paginationAtom)?.pages?.map((page, idx) => (
          <li key={page+idx}>
            {page === "..." ? (
              <span>{page}</span>
            ) : (
              <button
                className={ctx.get(pageAtom).get(ctx.get(countryAtom)) === page ? "active" : ""}
                onClick={() => updatePage(ctx, page)}
              >
                {page}
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}, "Pagination");

export default Pagination;
