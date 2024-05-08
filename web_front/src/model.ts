import { action, atom, batch, createCtx } from "@reatom/core";
import {
  reatomAsync,
  withDataAtom,
  withErrorAtom,
  onConnect,
  connectLogger,
} from "@reatom/framework";

export const ctx = createCtx();
connectLogger(ctx);

export const countries = [
  { name: "uzb", path: "/uzb", label: "Uzbek" },
  { name: "kaz", path: "/kaz", label: "Kazakh" },
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

export const countryAtom = atom("uzb", "countryAtom");
export const pageAtom = atom(new Map([[ctx.get(countryAtom), 1]]), "pageAtom");

export const updatePage = action((ctx, page: number) => {
  pageAtom(ctx, new Map([...ctx.get(pageAtom), [ctx.get(countryAtom), page]]));
});

export const updateCountry = action((ctx, country: string) => {
  countryAtom(ctx, country);
  pageAtom(ctx, new Map([[country, 1]]));
});

export const selectedColumnsAtom = atom(
  new Map(countries.map((country) => [country.name, [0, 1, 2]])),
  "selectedColumnsAtom",
);

export const updateSelectedColumns = action((ctx, column: number) => {
  const country = ctx.get(countryAtom);
  const selectedColumns = ctx.get(selectedColumnsAtom);
  column = Number(column);
  if (selectedColumns.has(country)) {
    if (selectedColumns.get(country).includes(column)) {
      selectedColumnsAtom(
        ctx,
        new Map([
          ...selectedColumns,
          [country, selectedColumns.get(country).filter((item) => item !== column)],
        ]),
      );
    } else {
      selectedColumnsAtom(
        ctx,
        new Map([
          ...selectedColumns,
          [country, [...selectedColumns.get(country), column].sort((a, b) => a - b)],
        ]),
      );
    }
  } else {
    selectedColumnsAtom(ctx, new Map([...selectedColumns, [country, [column]]]));
  }
});

const ApiUrl = "http://localhost:8000";
const apiUrlAtom = atom((ctx) => {
  const page = ctx.spy(pageAtom);
  const country = ctx.spy(countryAtom);

  let urlAtom = `${ApiUrl}`;

  if (country === "") {
    urlAtom = `${ApiUrl}/uzb`;
  }
  if (country !== "") {
    urlAtom = `${urlAtom}/${country.toLowerCase()}`;
  }
  if (page.has(country) && page.get(country) !== 0) {
    urlAtom = `${urlAtom}?page=${page.get(country)}`;
  }
  return urlAtom;
}, "apiUrlAtom");

export const fetchData = reatomAsync(async (ctx) => {
  const url = ctx.get(apiUrlAtom);
  const response = await fetch(url);
  console.log("fetchData", url);
  if (!response.ok) {
    throw new Error("Data Not Found");
  }
  return await response.json();
}, "fetchData").pipe(
  withErrorAtom((ctx, error) => "Data Not Found"),
  withDataAtom(new Map(), (ctx, data, state) => {
    // columnsAtom(ctx, data.columns);
    // selectedColumnsAtom(ctx, new Map([[ctx.get(countryAtom), [0, 1, 2]]]));
    return new Map([...state, [ctx.get(countryAtom), data]]);
  }),
);

// export const columnsAtom = atom((ctx) => ctx.spy(fetchData.dataAtom)?.columns || [1, 2, 3], "columnsAtom");

export const paginationAtom = atom((ctx) => {
  const country = ctx.spy(countryAtom);
  const pages = ctx.spy(fetchData.dataAtom).get(country)?.pages;
  const page = ctx.spy(pageAtom).get(country);
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
    return { country, pages: pagesArray };
  }
}, "paginationAtom");

onConnect(fetchData, (ctx) => {
  fetchData(ctx);
});

pageAtom.onChange(fetchData);
countryAtom.onChange(fetchData);
