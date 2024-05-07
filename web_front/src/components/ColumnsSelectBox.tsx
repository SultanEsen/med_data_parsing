import React, { useState } from "react";
import { reatomComponent } from "@reatom/npm-react";
import { fetchData, updateSelectedColumns, selectedColumnsAtom, countryAtom } from "../model";

const ColumnsSelectBox = reatomComponent(({ ctx }) => {
  const [showModal, setShowModal] = useState(false);
  const selectedColsInd = ctx.spy(selectedColumnsAtom).get(ctx.get(countryAtom));
  const country = ctx.spy(countryAtom);
  const columns = ctx.spy(fetchData.dataAtom).get(country)?.columns

  const selectColumns = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    updateSelectedColumns(ctx, Number(target.value));
  };

  return (
    <div className="columns">
      <button className="columns-btn" onClick={() => setShowModal(!showModal)}>
        Columns
      </button>
      <div className={`columns-modal ${showModal ? "show" : ""}`}>
        <div className="columns-container">
          {columns.map((column, ind) => (
            <label>
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
          <button className="columns-btn" onClick={() => setShowModal(!showModal)}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
});

export default ColumnsSelectBox;
