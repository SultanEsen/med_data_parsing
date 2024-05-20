// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import { reatomComponent } from "@reatom/npm-react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";

import { fetchData, countryAtom, selectedColumnsAtom } from "../model";

const DataTable = reatomComponent(({ ctx }) => {
  const country = ctx.spy(countryAtom);
  const dataRows = ctx.spy(fetchData.dataAtom).get(country)?.data;
  const selectedColsInd = ctx.spy(selectedColumnsAtom).get(country);
  const colNames = ctx.spy(fetchData.dataAtom).get(country)?.columns;

  if (ctx.spy(fetchData.pendingAtom)) {
    return (
      <div className="space-y-2">
        <Skeleton className="w-full h-8" />
        <Skeleton className="w-full h-8" />
        <Skeleton className="w-full h-8" />
      </div>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow className="bg-slate-100 text-slate-700">
          {colNames &&
            selectedColsInd.map((col) => (
              <TableHead key={col}>{colNames[col].replace(/_/g, " ")}</TableHead>
            ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {dataRows &&
          colNames &&
          dataRows?.map((row) => (
            <TableRow key={row.id} className="odd:bg-white even:bg-slate-50">
              {selectedColsInd.map((col) => (
                <TableCell key={col}>{row[colNames[col]]}</TableCell>
              ))}
            </TableRow>
          ))}
      </TableBody>
    </Table>
    // {/* <table> */}
    // {/*   <thead> */}
    // {/*     <tr id="table-header"> */}
    // {/*       {selectedColsInd.map((col) => ( */}
    // {/*         <th key={col}>{colNames[col].replace(/_/g, " ")}</th> */}
    // {/*       ))} */}
    // {/*     </tr> */}
    // {/*   </thead> */}
    // {/*   <tbody> */}
    // {/*     {dataRows?.map((row) => ( */}
    // {/*       <tr key={row.id}> */}
    // {/*         {selectedColsInd.map((col) => ( */}
    // {/*           <td key={col}>{row[colNames[col]]}</td> */}
    // {/*         ))} */}
    // {/*       </tr> */}
    // {/*     ))} */}
    // {/*   </tbody> */}
    // {/* </table> */}
  );
}, "DataTable");

export default DataTable;
