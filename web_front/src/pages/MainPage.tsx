import { reatomComponent } from "@reatom/npm-react";
import { paginationAtom, countryAtom, fetchData } from "../model";

import PagesList from "../components/PagesList";
import DataTable from "../components/DataTable";
import CountriesList from "../components/CountriesList";
// import SearchDialog from "../components/Search";
import ControlButtons from "../components/ControlButtons";

const MainPage = reatomComponent(({ ctx }) => {
  const showPaginationColumns =
    !ctx.spy(fetchData.errorAtom) && ctx.spy(paginationAtom).country === ctx.get(countryAtom);
  const showError = ctx.spy(fetchData.errorAtom);
  const showData = ctx.spy(fetchData.dataAtom)?.get(ctx.get(countryAtom));

  return (
    <div className="app">
      <div className="container">
        <div className="w-full flex flex-col gap-2 mb-2 sticky top-0 left-0 right-0 z-10 bg-white border-b p-3">
          <CountriesList />
          {showPaginationColumns && (
            <div className="flex gap-2 justify-between">
              <PagesList />
              {showData && showData!="undefined" && <ControlButtons />}
            </div>
          )}
        </div>
        <div className="w-full">
          {showError && <div id="error">{ctx.spy(fetchData.errorAtom)}</div>}
          {showData && showData!="undefined" && <DataTable />}
        </div>
      </div>
    </div>
  );
}, "MainPage");

export default MainPage;
