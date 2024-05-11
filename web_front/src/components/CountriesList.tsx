import React from "react";
import { reatomComponent } from "@reatom/npm-react";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { countries, updateCountry, type Countries } from "../model";

const CountriesList = reatomComponent(({ ctx }) => {
  const changeCountry = (e: React.MouseEvent<HTMLButtonElement>) => {
    const country = e.currentTarget.dataset.country;
    if (country) {
      updateCountry(ctx, country as Countries);
    }
  };

  return (
    <div className="w-fit p-2 m-1">
      <Tabs defaultValue={countries[0].name} className="w-[400px]">
        <TabsList>
          {countries.map((c) => (
            <TabsTrigger onClick={changeCountry} key={c.path} data-country={c.name} value={c.name}>
              {c.label}
            </TabsTrigger>
          ))}
        </TabsList>
        {/* <TabsContent value="account">Make changes to your account here.</TabsContent> */}
        {/* <TabsContent value="password">Change your password here.</TabsContent> */}
      </Tabs>
    </div>
  );
}, "CountriesList");

export default CountriesList;
