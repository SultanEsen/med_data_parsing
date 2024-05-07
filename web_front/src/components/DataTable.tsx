import { reatomComponent } from "@reatom/npm-react";

import { fetchData, countryAtom, selectedColumnsAtom } from "../model";

const DataTable = reatomComponent(({ ctx }) => {
  const country = ctx.spy(countryAtom);
  const dataRows = ctx.spy(fetchData.dataAtom).get(country)?.data;
  const selectedColsInd = ctx.spy(selectedColumnsAtom).get(country);
  const colNames = ctx.spy(fetchData.dataAtom).get(country)?.columns;

  console.log(selectedColsInd, "selectedColsInd");
  console.log(colNames, "colNames");

  return (
    <table>
      <thead>
        <tr id="table-header">
          {selectedColsInd.map((col) => (
            <th key={col}>{colNames[col].replace(/_/g, " ")}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {dataRows?.map((row) => (
          <tr key={row.id}>
            {selectedColsInd.map((col) => (
              <td key={col}>{row[colNames[col]]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}, "DataTable");

export default DataTable;
