import { useState } from "react";

type Props = {
  onSearch: (
    query: string
  ) => void;
  disabled?: boolean;
};

function SearchBar({
  onSearch,
  disabled
}: Props) {

  const [query, setQuery] =
    useState("");

  const handleSearch = () => {

    const cleanedQuery =
      query.trim();

    if (
      cleanedQuery.length < 2
    ) {

      alert(
        "Please enter at least 2 characters."
      );

      return;
    }

    onSearch(
      cleanedQuery
    );
  };

  return (

    <div className="bg-white rounded-2xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-4">
        Search Video
      </h2>

      <p className="text-gray-500 mb-4">
        Search by objects,
        scenes or spoken words.
      </p>

      <div className="flex gap-3">

        <input
          type="text"
          value={query}
          placeholder="e.g. person, road, nature..."
          onChange={(e) =>
            setQuery(
              e.target.value
            )
          }
          className="
          flex-1
          border
          rounded-lg
          p-3
          outline-none
          "
        />

        <button
          disabled={disabled}
          onClick={handleSearch}
          className="
          bg-green-600
          hover:bg-green-700
          text-white
          px-6
          rounded-lg
          font-medium
          disabled:bg-gray-400
          disabled:cursor-not-allowed
          "
        >
          Search
        </button>

      </div>

    </div>
  );
}

export default SearchBar;