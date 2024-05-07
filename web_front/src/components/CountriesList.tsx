import React from "react";
import { reatomComponent } from "@reatom/npm-react";

import { countries, countryAtom, updateCountry } from "../model";


const CountriesList = reatomComponent(({ ctx }) => {
  const changeCountry = (e: React.MouseEvent) => {
    const country = (e.target as HTMLButtonElement).dataset.country;
    if (country) {
      updateCountry(ctx, country);
    }
  };

  return (
    <div className="buttons-list">
      <ul id="countries">
        {countries.map((c) => (
          <li key={c.path}>
            <button
              className={ctx.get(countryAtom).toLowerCase() === c.name ? "active" : ""}
              data-country={c.name}
              onClick={changeCountry}
            >
              {c.label}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}, "CountriesList");

export default CountriesList;
