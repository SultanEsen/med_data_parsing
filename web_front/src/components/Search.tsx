import { useRef, useEffect } from "react";

import SearchForm from "./SearchForm";

const SearchDialog = ({ showModal, setShowModal }) => {
  const ref = useRef();

  useEffect(() => {
    if (showModal) {
      ref.current.showModal();
    } else {
      ref.current.close();
    }
  }, [showModal]);

  return (
    <dialog ref={ref}>
      <SearchForm setShowModal={setShowModal} />
    </dialog>
  );
};

export default SearchDialog;
