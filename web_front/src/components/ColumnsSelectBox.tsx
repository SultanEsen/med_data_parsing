import React, { useState } from "react";
import { reatomComponent } from "@reatom/npm-react";
import { columnsAtom, updateSelectedColumns } from "../model";

const ColumnsSelectBox = reatomComponent(({ ctx }) => {
  const [showModal, setShowModal] = useState(false);

  const selectColumns = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    updateSelectedColumns(ctx, target.value);
  };

  return (
    <div className="columns">
      <button className="columns-btn" onClick={() => setShowModal(!showModal)}>
        Columns
      </button>
      <div className={`columns-modal ${showModal ? "show" : ""}`}>
        <div className="columns-container">
          {ctx.spy(columnsAtom).map((column) => (
            <label>
              <input type="checkbox" key={column} value={column} onChange={selectColumns} />
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
