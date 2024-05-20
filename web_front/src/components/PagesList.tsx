import { useState } from "react";
import { reatomComponent } from "@reatom/npm-react";

import { pageAtom, countryAtom, updatePage, fetchData } from "../model";
import { dictionaryAtom } from "@/translation-model";
import { Button } from "@/components/ui/button";

const PagesList = reatomComponent(({ ctx }) => {
  let currentPage = ctx.spy(pageAtom).get(ctx.get(countryAtom));
  if (currentPage === undefined) {
    currentPage = 1;
  }
  const totalPages = ctx.spy(fetchData.dataAtom).get(ctx.get(countryAtom))?.pages;
  const [editPage, setEditPage] = useState(false);
  const [newPage, setNewPage] = useState<number>(1);

  const changePage = (page: number) => {
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
            onChange={(e) => setNewPage(Number(e.target.value))}
            onKeyUp={(e: React.KeyboardEvent) => {
              if (e.key === "Enter") changePage(newPage);
            }}
            defaultValue={currentPage}
            autoFocus
          />
          <Button variant="outline" onClick={() => changePage(newPage)}>
            {ctx.spy(dictionaryAtom)?.["go"]}
          </Button>
        </div>
      ) : (
        <div className="flex gap-2 items-center justify-center">
          <Button variant="outline" onClick={() => updatePage(ctx, currentPage - 1)}>
            {ctx.spy(dictionaryAtom)?.["prev"]}
          </Button>
          <span className="cursor-pointer w-[100px] text-center" onClick={() => setEditPage(true)}>
            {currentPage} / {totalPages}
          </span>
          <Button variant="outline" onClick={() => updatePage(ctx, currentPage + 1)}>
            {ctx.spy(dictionaryAtom)?.["next"]}
          </Button>
        </div>
      )}
    </div>
  );
}, "Pagination");

export default PagesList;
