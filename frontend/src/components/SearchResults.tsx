import type {
  SearchResponse
} from "../types/search";

type Props = {
  results: SearchResponse | null;
};

function SearchResults({
  results,
}: Props) {

  if (!results) {
    return null;
  }

  const noResults =

    results.clip_results.length === 0 &&

    results.yolo_results.length === 0 &&

    results.transcript_results.length === 0;

    if (noResults) {

        return (

            <div
                className="
                bg-white
                rounded-2xl
                shadow
                p-8
                text-center
                "
            >

            <div className="text-5xl mb-4">

                🔍

            </div>

            <h3
                className="
                    text-2xl
                    font-bold
                    mb-2
                    "
            >

                No Results Found

            </h3>

            <p className="text-gray-500">

                Try searching for:

            </p>

            <div
                className="
                mt-4
                flex
                justify-center
                gap-3
                flex-wrap
                "
            >

                <span className="px-3 py-1 bg-gray-100 rounded-full">
                    person
                </span>

                <span className="px-3 py-1 bg-gray-100 rounded-full">
                    road
                </span>

                <span className="px-3 py-1 bg-gray-100 rounded-full">
                    nature
                </span>

                <span className="px-3 py-1 bg-gray-100 rounded-full">
                    child
                </span>

            </div>

            </div>

        );
    }

  return (

    <div className="space-y-8">

      {/* CLIP */}

      <div>

        <h3 className="text-2xl font-bold mb-4">

          Semantic Results
            ({results.clip_results.length})
        </h3>

        <div className="grid md:grid-cols-2 gap-4">

          {results.clip_results.map(
            (item, index) => (

              <div
                key={index}
                className="
                border
                rounded-xl
                p-4
                bg-slate-50
                "
              >

                <img
                    src={`http://127.0.0.1:8000/frames/${item.frame}`}
                    alt={item.frame}
                    className="
                    w-full
                    h-48
                    object-cover
                    rounded-lg
                    mb-3
                    "
                />

                <p className="font-semibold">
                    {item.frame}
                </p>

                <p className="text-gray-500">

                  Similarity:
                  {" "}
                  {(item.similarity * 100)
                    .toFixed(2)}%

                </p>

                <p className="text-gray-500">

                    ⏱
                    {" "}
                    {item.timestamp}s

                </p>

              </div>
            )
          )}

        </div>

      </div>

      {/* YOLO */}

      <div>

        <h3 className="text-2xl font-bold mb-4">

          Object Detection Results
            ({results.yolo_results.length})

        </h3>

        <div className="grid md:grid-cols-2 gap-4">

          {results.yolo_results.map(
            (item, index) => (

                <div
                key={index}
                className="
                border
                rounded-xl
                p-4
                bg-slate-50
                "
                >

                <img
                    src={`http://127.0.0.1:8000/frames/${item.frame}`}
                    alt={item.frame}
                    className="
                    w-full
                    h-48
                    object-cover
                    rounded-lg
                    mb-3
                    "
                />

                <p className="font-semibold">
                    {item.frame}
                </p>

                <p className="text-gray-500">
                    ⏱ {item.timestamp}s
                </p>

                </div>

            )
            )}

        </div>

      </div>

      {/* TRANSCRIPT */}

      <div>

        <h3 className="text-2xl font-bold mb-4">

          Transcript Results
            ({results.transcript_results.length})

        </h3>

        <div className="space-y-4">

          {results.transcript_results.map(
            (item, index) => (

              <div
                key={index}
                className="
                border
                rounded-xl
                p-4
                bg-slate-50
                "
              >

                <p className="font-semibold">

                    ⏱ {item.start.toFixed(2)}s

                </p>

                <p className="mt-2">

                  {item.text}

                </p>

              </div>
            )
          )}

        </div>

      </div>

    </div>
  );
}

export default SearchResults;