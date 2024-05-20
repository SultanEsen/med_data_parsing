import React from "react";
import { reatomComponent } from "@reatom/npm-react";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { countries, countryAtom, type CountryType } from "../model";
import { dictionaryAtom } from "@/translation-model";

const CountriesList = reatomComponent(({ ctx }) => {
  const changeCountry = (e: React.MouseEvent<HTMLButtonElement>) => {
    const country = e.currentTarget.dataset.country;
    if (country) {
      countryAtom(ctx, country as CountryType);
    }
  };

  return (
    <div className="w-fit py-2 my-1">
      <Tabs defaultValue={countries[0].name}>
        <TabsList>
          {countries.map((c) => (
            <TabsTrigger onClick={changeCountry} key={c.path} data-country={c.name} value={c.name}>
              {ctx.spy(dictionaryAtom)?.[c.label]}
            </TabsTrigger>
          ))}
        </TabsList>
        {/* <TabsContent value="password">Change your password here.</TabsContent> */}
      </Tabs>
    </div>
  );
}, "CountriesList");

export default CountriesList;
