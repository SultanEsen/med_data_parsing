// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import React, { useState } from "react";
import { reatomComponent } from "@reatom/npm-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

import {
  fetchData,
  updateSelectedColumns,
  selectedColumnsAtom,
  countryAtom,
  countries,
} from "../model";

const ControlButtons = reatomComponent(({ ctx }) => {
  const [showModal, setShowModal] = useState(false);
  const selectedColsInd = ctx.spy(selectedColumnsAtom).get(ctx.get(countryAtom));
  const country = ctx.spy(countryAtom);
  const columns = ctx.spy(fetchData.dataAtom).get(country)?.columns;

  const selectColumns = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    updateSelectedColumns(ctx, Number(target.value));
  };

  return (
    <div className="flex gap-2">
      <Button>Search</Button>
      <Dialog>
        <DialogTrigger asChild>
          <Button>Select Columns</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>
              Select columns for {countries.filter((c) => c.name === country)?.[0]?.label}
            </DialogTitle>
          </DialogHeader>
          <div className="flex flex-col gap-2">
            {columns &&
              columns.map((column, ind: number) => (
                <label key={column} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    key={column}
                    value={ind}
                    onChange={selectColumns}
                    checked={selectedColsInd.includes(ind)}
                  />
                  {column}
                </label>
              ))}
          </div>
          <DialogFooter className="sm:justify-start">
            <DialogClose asChild>
              <Button type="button">OK</Button>
            </DialogClose>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      <Tabs defaultValue="raw">
        <TabsList>
          <TabsTrigger value="raw">Raw Data</TabsTrigger>
          <TabsTrigger value="prep">Prepared</TabsTrigger>
        </TabsList>
      </Tabs>
    </div>
  );
});

export default ControlButtons;
