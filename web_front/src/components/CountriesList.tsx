import { reatomComponent } from "@reatom/npm-react";

import { countryAtom } from "../model";

const CountriesList = reatomComponent(({ ctx }) => {
  const changeCountry = (e: Event) => {
    const country = (e.target as HTMLButtonElement).dataset.country;
    if (country) {
      countryAtom(ctx, country);
    }
  };

  return (
    <div>
      <ul id="countries">
        <li>
          <button data-country="Uzb" onClick={changeCountry}>
            Uzb
          </button>
        </li>
        <li>
          <button data-country="Kaz" onClick={changeCountry}>
            Kaz
          </button>
        </li>
        <li>
          <button data-country="Rus" onClick={changeCountry}>
            Russia
          </button>
        </li>
        <li>
          <button data-country="Blr" onClick={changeCountry}>
            Belarus
          </button>
        </li>
        <li>
          <button data-country="Tur" onClick={changeCountry}>
            Turkey
          </button>
        </li>
        <li>
          <button data-country="Mld" onClick={changeCountry}>
            Moldova
          </button>
        </li>
      </ul>
    </div>
  );
}, "CountriesList");

export default CountriesList;
