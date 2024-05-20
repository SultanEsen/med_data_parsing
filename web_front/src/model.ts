import { action, atom, createCtx } from "@reatom/core";
import {
  reatomAsync,
  withDataAtom,
  withErrorAtom,
  withAbort,
  onConnect,
  connectLogger,
  isShallowEqual,
} from "@reatom/framework";


export const ctx = createCtx();
connectLogger(ctx);

export type CountryType = "uzb" | "kaz" | "rus" | "blr" | "ukr" | "turk" | "mld";
export type CountryName = "Uzbekistan" | "Kazakhstan" | "Russia" | "Belarus" | "Ukraine" | "Turkey" | "Moldova";

export const countries: { name: CountryType; path: string; label: CountryName }[] = [
  { name: "uzb", path: "/uzb", label: "Uzbekistan" },
  { name: "kaz", path: "/kaz", label: "Kazakhstan" },
  { name: "rus", path: "/rus", label: "Russia" },
  { name: "blr", path: "/blr", label: "Belarus" },
  { name: "ukr", path: "/ukr", label: "Ukraine" },
  { name: "turk", path: "/turk", label: "Turkey" },
  { name: "mld", path: "/mld", label: "Moldova" },
];

const ApiUrl = import.meta.env.VITE_API_ADDRESS;


export const pathAtom = atom("/", "path");
export const redirect = action((ctx, path: string) => {
  pathAtom(ctx, path);
  window.location.pathname = path;
});

export const countryAtom = atom<CountryType>("uzb", "countryAtom");
export const pageAtom = atom(new Map<CountryType, number>(countries.map((country) => [country.name, 1])), "pageAtom");


export const selectedColumnsAtom = atom(
  new Map<CountryType, number[]>(countries.map((country) => [country.name, [0, 1, 2]])),
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


export const fetchData = reatomAsync(async (ctx) => {
  const page = ctx.get(pageAtom);
  const country = ctx.get(countryAtom);

  let url = `${ApiUrl}`;

  url = `${url}/${country}`;
  if (page.has(country) && page.get(country) !== 0) {
    url = `${url}?page=${page.get(country)}`;
  }
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

export const updatePage = action((ctx, page: number) => {
  if (page < 1) {
    page = 1;
  }
  const totalPages = ctx.get(fetchData.dataAtom)?.get(ctx.get(countryAtom))?.pages || 1;
  if (page > totalPages) {
    page = totalPages;
  }
  const newState = new Map([...ctx.get(pageAtom), [ctx.get(countryAtom), page]]);
  if (!isShallowEqual(ctx.get(pageAtom), newState)) {
    pageAtom(ctx, newState);
  }
});

onConnect(fetchData, (ctx) => {
  fetchData(ctx);
});

pageAtom.onChange(fetchData);
countryAtom.onChange(fetchData);
