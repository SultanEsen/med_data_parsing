import { reatomComponent } from "@reatom/npm-react";

import { countryAtom, updateCountry } from "../model";

const countries = {
  Uzb: "Uzbek",
  Kaz: "Kaz",
  Rus: "Russia",
  Blr: "Belarus",
  Turk: "Turkey",
  Mld: "Moldova",
};

const CountriesList = reatomComponent(({ ctx }) => {
  const changeCountry = (e: Event) => {
    const country = (e.target as HTMLButtonElement).dataset.country;
    if (country) {
      updateCountry(ctx, country);
    }
  };

  return (
    <div class="buttons-list">
      <ul id="countries">
        {Object.keys(countries).map((key) => (
          <li key={key}>
            <button
              class={ctx.get(countryAtom) === key ? "active" : ""}
              data-country={key}
              onClick={changeCountry}
            >
              {countries[key]}
            </button>
          </li>
        ))}
        {/* <li> */}
        {/*   <button data-country="Uzb" onClick={changeCountry}> */}
        {/*     Uzb */}
        {/*   </button> */}
        {/* </li> */}
        {/* <li> */}
        {/*   <button data-country="Kaz" onClick={changeCountry}> */}
        {/*     Kaz */}
        {/*   </button> */}
        {/* </li> */}
        {/* <li> */}
        {/*   <button data-country="Rus" onClick={changeCountry}> */}
        {/*     Russia */}
        {/*   </button> */}
        {/* </li> */}
        {/* <li> */}
        {/*   <button data-country="Blr" onClick={changeCountry}> */}
        {/*     Belarus */}
        {/*   </button> */}
        {/* </li> */}
        {/* <li> */}
        {/*   <button data-country="Turk" onClick={changeCountry}> */}
        {/*     Turkey */}
        {/*   </button> */}
        {/* </li> */}
        {/* <li> */}
        {/*   <button data-country="Mld" onClick={changeCountry}> */}
        {/*     Moldova */}
        {/*   </button> */}
        {/* </li> */}
        <li>
          <button>Documents</button>
        </li>
      </ul>
    </div>
  );
}, "CountriesList");

export default CountriesList;
