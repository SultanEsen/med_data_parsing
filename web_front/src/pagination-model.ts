import { action, atom } from "@reatom/core";

type Pagination = (number | "...")[];

export const paginationAtom = atom<Pagination>([],"paginationAtom");

export const updatePages = action((ctx, pages: number, page: number) => {
    let pagesArray;
  if (!pages || !page) {
    // return { country, pages: [] };
    return []
  }
  if (pages <= 5) {
    // return { country, pages: [1, 2, 3, 4, 5].splice(0, pages) };
    pagesArray = [1, 2, 3, 4, 5].splice(0, pages)
  } else {
    if (page <= 3) {
      pagesArray = [1, 2, 3, 4, "...", pages];
    } else if (page > 3 && page < pages - 2) {
      pagesArray = [1, "...", page - 1, page, page + 1, "...", pages];
    } else if (page >= pages - 2) {
      pagesArray = [1, "...", pages - 3, pages - 2, pages - 1, pages];
    }
    // @ts-ignore
    paginationAtom(ctx, pagesArray);
  }
}, "updatePages");


