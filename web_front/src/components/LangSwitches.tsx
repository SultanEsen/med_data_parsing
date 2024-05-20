import { reatomComponent } from "@reatom/npm-react";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { languageAtom } from "@/translation-model";

const LangSwitches = reatomComponent(({ ctx }) => {
  return (
      <Tabs defaultValue="en">
        <TabsList>
          <TabsTrigger value="en" onClick={() => languageAtom(ctx, "en")}>EN</TabsTrigger>
          <TabsTrigger value="ru" onClick={() => languageAtom(ctx, "ru")}>RU</TabsTrigger>
        </TabsList>
      </Tabs>
  )
}, "LangSwitches");

export default LangSwitches
