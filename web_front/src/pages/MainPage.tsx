// import { useState } from "react";
import { reatomComponent } from "@reatom/npm-react";
import { redirect, paginationAtom, countryAtom, fetchData } from "../model";

import Pagination from "../components/Pagination";
import DataTable from "../components/DataTable";
import CountriesList from "../components/CountriesList";
// import SearchDialog from "../components/Search";

const MainPage = reatomComponent(({ ctx }) => {
  // const [showModal, setShowModal] = useState(false);

  const showPagination =
    !ctx.spy(fetchData.errorAtom) && ctx.spy(paginationAtom).country === ctx.get(countryAtom);
  const showError = ctx.spy(fetchData.errorAtom);
  const showData = ctx.spy(fetchData.dataAtom)?.get(ctx.get(countryAtom));

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h4>Index Page with data from sources</h4>
          <CountriesList />
          {/* <button onClick={() => redirect(ctx, "/search")}>Search</button> */}
          {showPagination && <Pagination />}
        </div>
        {/* <SearchDialog showModal={showModal} setShowModal={setShowModal} /> */}
        {showError && <div id="error">{ctx.spy(fetchData.errorAtom)}</div>}
        {showData && <DataTable />}
      </div>
    </div>
  );
}, "MainPage");

export default MainPage;
