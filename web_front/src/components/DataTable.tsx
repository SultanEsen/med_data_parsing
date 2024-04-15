import { reatomComponent } from "@reatom/npm-react";

import { fetchData, countryAtom } from "../model";

const DataTable = reatomComponent(({ ctx }) => {
  const dataRows = ctx.spy(fetchData.dataAtom).get(ctx.get(countryAtom))?.data;

  return (
    <table>
      <thead>
        <tr id="table-header"></tr>
      </thead>
      <tbody>
        {dataRows?.map((row) => (
          <tr key={row.id}>
            <td>{row.id}</td>
            <td>{row.package_id}</td>
            <td>{row.trade_mark_name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}, "DataTable");

export default DataTable;
