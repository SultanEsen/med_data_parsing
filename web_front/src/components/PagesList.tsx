import { reatomComponent } from "@reatom/npm-react";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

import { pageAtom, paginationAtom, countryAtom, updatePage } from "../model";

const PagesList = reatomComponent(({ ctx }) => {
  return (
    <div className="pagination-container">
      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious href="#" />
          </PaginationItem>
          {ctx.spy(paginationAtom)?.pages?.map((page) => (
            <PaginationItem>
              {page === "..." ? (
                <PaginationEllipsis />
              ) : (
                <PaginationLink
                  isActive={ctx.get(pageAtom).get(ctx.get(countryAtom)) === page}
                  onClick={() => updatePage(ctx, page)}
                >
                  {page}
                </PaginationLink>
              )}
            </PaginationItem>
          ))}
          <PaginationItem>
            <PaginationNext href="#" />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
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
