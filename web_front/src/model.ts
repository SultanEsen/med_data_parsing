import { action, batch, atom, createCtx } from "@reatom/core";
import {
  reatomAsync,
  withDataAtom,
  withErrorAtom,
  withAbort,
  onConnect,
  connectLogger,
} from "@reatom/framework";

export const ctx = createCtx();
connectLogger(ctx);

export type Countries = "uzb" | "kaz" | "rus" | "blr" | "ukr" | "turk" | "mld";

export const countries: { name: Countries; path: string; label: string }[] = [
  { name: "uzb", path: "/uzb", label: "Uzbekistan" },
  { name: "kaz", path: "/kaz", label: "Kazakhstan" },
  { name: "rus", path: "/rus", label: "Russia" },
  { name: "blr", path: "/blr", label: "Belarus" },
  { name: "ukr", path: "/ukr", label: "Ukraine" },
  { name: "turk", path: "/turk", label: "Turkey" },
  { name: "mld", path: "/mld", label: "Moldova" },
];

export const pathAtom = atom("/", "path");
export const redirect = action((ctx, path: string) => {
  pathAtom(ctx, path);
  window.location.pathname = path;
});

export const countryAtom = atom<Countries>("uzb", "countryAtom");
export const pageAtom = atom(new Map([[ctx.get(countryAtom), 1]]), "pageAtom");

export const updatePage = action((ctx, page: number) => {
  pageAtom(ctx, new Map([...ctx.get(pageAtom), [ctx.get(countryAtom), page]]));
});

export const updateCountry = action((ctx, country: Countries) => {
  // batch(ctx, () => {
    countryAtom(ctx, country);
    // pageAtom(ctx, new Map([...ctx.get(pageAtom), [country, 1]]));
  // })
});

export const selectedColumnsAtom = atom(
  new Map<Countries, number[]>(countries.map((country) => [country.name, [0, 1, 2]])),
  "selectedColumnsAtom",
);

export const updateSelectedColumns = action((ctx, column: number) => {
  const country = ctx.get(countryAtom);
  const selectedColumns = ctx.get(selectedColumnsAtom);
  const countryColumns = selectedColumns.get(country);
  column = Number(column);
  if (countryColumns && countryColumns.includes(column)) {
      selectedColumnsAtom(
        ctx,
        new Map([
          ...selectedColumns,
          [country, countryColumns.filter((item) => item !== column)],
        ]),
      );
  } else if (countryColumns) {
    
      selectedColumnsAtom(
        ctx,
        new Map([
          ...selectedColumns,
          [country, [...countryColumns, column].sort((a, b) => a - b)],
        ]),
      );
  } else {
    selectedColumnsAtom(ctx, new Map([...selectedColumns, [country, [column]]]));
  }
});

const ApiUrl = import.meta.env.VITE_API_ADDRESS;
const apiUrlAtom = atom((ctx) => {
  const page = ctx.spy(pageAtom);
  const country = ctx.spy(countryAtom);

  let urlAtom = `${ApiUrl}`;

  // if (country === "") {
  //   urlAtom = `${ApiUrl}/uzb`;
  // }
  // if (country !== "") {
    urlAtom = `${urlAtom}/${country}`;
  // }
  if (page.has(country) && page.get(country) !== 0) {
    urlAtom = `${urlAtom}?page=${page.get(country)}`;
  }
  return urlAtom;
}, "apiUrlAtom");

export const paginationAtom = atom({country: "", pages: []} ,"paginationAtom");

export const updatePages = action((ctx, pages: number, page: number, country: Countries) => {
  // const country = ctx.get(countryAtom);
  // const pages = ctx.spy(fetchData.dataAtom).get(country)?.pages;
  // const allData = ctx.get(fetchData.dataAtom);
  // const country = ctx.get(countryAtom);
  // const pages = allData.get(country)?.pages;
  // const page = ctx.get(pageAtom).get(country);
  if (!pages || !page) {
    return { country, pages: [] };
  }
  if (pages <= 5) {
    return { country, pages: [1, 2, 3, 4, 5].splice(0, pages) };
  } else {
    let pagesArray;
    if (page <= 3) {
      pagesArray = [1, 2, 3, 4, "...", pages];
    } else if (page > 3 && page < pages - 2) {
      pagesArray = [1, "...", page - 1, page, page + 1, "...", pages];
    } else if (page >= pages - 2) {
      pagesArray = [1, "...", pages - 3, pages - 2, pages - 1, pages];
    }
    paginationAtom(ctx, { country, pages: pagesArray });
  }
}, "updatePages");


export const fetchData = reatomAsync(async (ctx) => {
  const page = ctx.get(pageAtom);
  const country = ctx.get(countryAtom);

  let url = `${ApiUrl}`;

  // if (country === "") {
  //   urlAtom = `${ApiUrl}/uzb`;
  // }
  // if (country !== "") {
    url = `${url}/${country}`;
  // }
  if (page.has(country) && page.get(country) !== 0) {
    url = `${url}?page=${page.get(country)}`;
  }
  // const url = ctx.get(apiUrlAtom);
  console.log("fetchData", url);
  const response = await fetch(url, ctx.controller);
  if (!response.ok) {
    throw new Error("Data Not Found");
  }
  return await response.json();
}, "fetchData").pipe(
  withErrorAtom(() => "Data Not Found"),
  withDataAtom(new Map(), (ctx, data, state) => {
    return new Map([...state, [ctx.get(countryAtom), data]]);
  }),
  withAbort()
);

fetchData.onFulfill.onCall((ctx) => {
  const allData = ctx.get(fetchData.dataAtom);
  const country = ctx.get(countryAtom);
  const pages = allData.get(country)?.pages;
  let page = Number(ctx.get(pageAtom).get(country));
  if (!page || typeof page == "undefined") {
    page = 1;
  }
  updatePages(ctx, pages, page, country); 
})


onConnect(fetchData, (ctx) => {
  fetchData(ctx);
});

pageAtom.onChange(fetchData);
countryAtom.onChange(fetchData);
