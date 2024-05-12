import { reatomComponent } from "@reatom/npm-react";
import { countryAtom, fetchData } from "../model";
import { Skeleton } from "@/components/ui/skeleton";

import PagesList from "@/components/PagesList";
import DataTable from "@/components/DataTable";
import CountriesList from "@/components/CountriesList";
import ControlButtons from "@/components/ControlButtons";
import LangSwitches from "@/components/LangSwitches";

const LowerMenu = reatomComponent(({ ctx }) => {
  const showPaginationColumns = !ctx.spy(fetchData.errorAtom);
  // const showData = ctx.spy(fetchData.dataAtom)?.get(ctx.get(countryAtom));

  if (ctx.spy(fetchData.pendingAtom)) {
    return <Skeleton className="w-full h-8" />;
  }

  return (
    <div className="flex gap-2 justify-between">
      {showPaginationColumns && (
        <>
          <PagesList />
          <ControlButtons />
        </>
      )}
    </div>
  );
});

const MainPage = reatomComponent(({ ctx }) => {
  const showError = ctx.spy(fetchData.errorAtom);
  const showData = ctx.spy(fetchData.dataAtom)?.get(ctx.get(countryAtom));

  return (
    <div className="app">
      <div className="container">
        <div className="w-full flex flex-col gap-2 mb-2 sticky top-0 left-0 right-0 z-10 bg-white border-b p-3">
          <div className="flex gap-2 justify-between w-full items-center">
            <CountriesList />
            <LangSwitches />
          </div>
          <LowerMenu />
        </div>
        <div className="w-full">
          {showError && (
            <div id="error" className="text-red-500 w-full text-center">
              <h4>{ctx.spy(fetchData.errorAtom)}</h4>
            </div>
          )}
          {showData && showData != "undefined" && <DataTable />}
        </div>
      </div>
    </div>
  );
}, "MainPage");

export default MainPage;
