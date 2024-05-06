import { reatomComponent } from "@reatom/npm-react";

import { countryAtom, updateCountry } from "../model";

const countries = [
  {  path: "/uzb", label: "uzbek"},
  {  path: "/kaz", label: "kazakh"},
  {  path: "/rus", label: "russia"},
  {  path: "/blr", label: "belarus"},
  {  path: "/ukr", label: "ukraine"},
  {  path: "/turk", label: "turkey"},
  {  path: "/mld", label: "moldova"},
];

const CountriesList = reatomComponent(({ ctx }) => {
  const changeCountry = (e: Event) => {
    const country = (e.target as HTMLButtonElement).dataset.country;
    if (country) {
      updateCountry(ctx, country);
    }
  };

  return (
  
  )

  // return (
    {/* <div className="buttons-list"> */}
      {/* <ul id="countries"> */}
      {/*   {Object.keys(countries).map((key) => ( */}
      {/*     <li key={key}> */}
      {/*       <button */}
      {/*         className={ctx.get(countryAtom) === key ? "active" : ""} */}
      {/*         data-country={key} */}
      {/*         onClick={changeCountry} */}
      {/*       > */}
      {/*         {countries[key]} */}
      {/*       </button> */}
      {/*     </li> */}
      {/*   ))} */}
      {/* </ul> */}
    // </div>
  // );
}, "CountriesList");

export default CountriesList;
