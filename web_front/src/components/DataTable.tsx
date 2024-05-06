import { reatomComponent } from "@reatom/npm-react";

import { fetchData, countryAtom, selectedColumnsAtom } from "../model";

const DataTable = reatomComponent(({ ctx }) => {
  const dataRows = ctx.spy(fetchData.dataAtom).get(ctx.get(countryAtom))?.data;
  const cols = ctx.spy(selectedColumnsAtom).get(ctx.get(countryAtom));

  return (
    <table>
      <thead>
        <tr id="table-header">
          {cols.map((col) => (
            <th key={col}>{col.replace(/_/g, " ")}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {dataRows?.map((row) => (
          <tr key={row.id}>
            {cols.map((col) => (
              <td key={col}>{row[col]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}, "DataTable");

export default DataTable;
