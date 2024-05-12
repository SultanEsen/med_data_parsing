import { useState } from "react";
import { reatomComponent } from "@reatom/npm-react";

import { pageAtom, countryAtom, updatePage, fetchData } from "../model";
import { Button } from "@/components/ui/button";

const PagesList = reatomComponent(({ ctx }) => {
  const currentPage = ctx.spy(pageAtom).get(ctx.get(countryAtom));
  const totalPages = ctx.spy(fetchData.dataAtom).get(ctx.get(countryAtom))?.pages;
  const [editPage, setEditPage] = useState(false);
  const [newPage, setNewPage] = useState<number>(currentPage);

  const changePage = (page: string) => {
    if (page === null) {
      return;
    }
    if (Number(page) > 0 && Number(page) <= totalPages) {
      updatePage(ctx, Number(page));
    }
    setEditPage(false);
  };

  return (
    <div className="flex gap-2 items-center">
      {editPage ? (
        <div className="flex gap-2 items-center">
          <input
            className="w-20"
            type="number"
            onChange={(e) => setNewPage(e.target.value)}
            onKeyUp={(e: React.KeyboardEvent) => {
              if (e.key === "Enter") changePage(newPage);
            }}
            defaultValue={currentPage}
            autoFocus
          />
          <Button variant="outline" onClick={() => changePage(newPage)}>
            GO
          </Button>
        </div>
      ) : (
        <div className="flex gap-2 items-center justify-center">
          <Button variant="outline" onClick={() => updatePage(ctx, currentPage - 1)}>
            prev
          </Button>
          <span className="cursor-pointer w-[100px] text-center" onClick={() => setEditPage(true)}>
            {currentPage} / {totalPages}
          </span>
          <Button variant="outline" onClick={() => updatePage(ctx, currentPage + 1)}>
            next
          </Button>
        </div>
      )}
      {/* <ul id="pagination"> */}
      {/*   {ctx.spy(paginationAtom)?.pages?.map((page, idx) => ( */}
      {/*     <li key={page+idx}> */}
      {/*       {page === "..." ? ( */}
      {/*         <span>{page}</span> */}
      {/*       ) : ( */}
      {/*         <button */}
      {/*           className={ctx.get(pageAtom).get(ctx.get(countryAtom)) === page ? "active" : ""} */}
      {/*           onClick={() => updatePage(ctx, page)} */}
      {/*         > */}
      {/*           {page} */}
      {/*         </button> */}
      {/*       )} */}
      {/*     </li> */}
      {/*   ))} */}
      {/* </ul> */}
    </div>
  );
}, "Pagination");

export default PagesList;
