import { reatomComponent } from "@reatom/npm-react";

import { fetchData, countryAtom, columnsAtom } from "../model";

const DataTable = reatomComponent(({ ctx }) => {
  const dataRows = ctx.spy(fetchData.dataAtom).get(ctx.get(countryAtom))?.data;
  const cols = ctx.spy(columnsAtom);

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
