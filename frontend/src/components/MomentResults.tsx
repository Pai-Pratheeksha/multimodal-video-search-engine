import type { Moment } from "../types/moment";

interface Props {

  results: Moment[];

  onJump:
    (
      moment: Moment
    ) => void;

    activeTimestamp:
        number | null;
}

const formatTimestamp = (
  seconds: number
) => {

  const mins = Math.floor(
    seconds / 60
  );

  const secs = Math.floor(
    seconds % 60
  );

  return `${mins
    .toString()
    .padStart(2, "0")}:${secs
    .toString()
    .padStart(2, "0")}`;
};

function MomentResults({
  results,
  onJump,
  activeTimestamp
}: Props) {

  if (!results.length) {

    return null;
  }

  return (

    <div className="mt-8">

      <h2 className="
      text-2xl
      font-bold
      mb-4
      ">

        Multimodal Results

      </h2>

      <div className="space-y-4">

        {results.map(
          (moment, index) => (

            <div
            key={index}
            className={`

            rounded-xl
            shadow
            p-5
            transition-all

            ${
                activeTimestamp ===
                moment.timestamp

                ? `
                bg-blue-50
                border-2
                border-blue-500
                `
                : `
                bg-white
                border
                `
            }
            `}
            >

              <h3 className="font-bold">

                Moment #{index + 1}

              </h3>

              {moment.thumbnail && (

                <img
                    src={
                    `http://127.0.0.1:8000/frames/${moment.thumbnail}`
                    }
                    alt="thumbnail"
                    className="
                    w-full
                    h-48
                    object-cover
                    rounded-lg
                    mb-4
                    "
                />

                )}

              <div className="mb-2">
                <span
                  className={`

                  px-3
                  py-1
                  rounded-full
                  text-sm
                  font-semibold

                  ${
                    moment.confidence === "high"
                      ? "bg-green-100 text-green-700"

                    : moment.confidence === "medium"
                      ? "bg-yellow-100 text-yellow-700"

                    : "bg-red-100 text-red-700"
                  }
                `}
                >

                  {moment.confidence.toUpperCase()}

                </span>
              </div>
              
              <p className="
                font-medium
                text-lg
                ">

                ⏱ {formatTimestamp(
                    moment.timestamp
                    )}

                </p>
                <p className="
                text-sm
                text-gray-500
                ">

                {moment.timestamp.toFixed(2)}s

                </p>

              <div className="flex flex-wrap gap-2 mb-3">

                {moment.clip_score > 0 && (

                    <span
                    className="
                    px-3
                    py-1
                    rounded-full
                    bg-blue-100
                    text-blue-700
                    text-sm
                    font-medium
                    "
                    >
                    Semantic Match
                    </span>

                )}

                {moment.yolo_match && (

                    <span
                    className="
                    px-3
                    py-1
                    rounded-full
                    bg-green-100
                    text-green-700
                    text-sm
                    font-medium
                    "
                    >
                    Object Match
                    </span>

                )}

                {moment.whisper_match && (

                    <span
                    className="
                    px-3
                    py-1
                    rounded-full
                    bg-purple-100
                    text-purple-700
                    text-sm
                    font-medium
                    "
                    >
                    Speech Match
                    </span>

                )}

                </div>

              <p>

                Score:
                {" "}
                {moment.score}

              </p>

              <button
                onClick={() =>
                    onJump(
                    moment
                    )
                }
                className="
                mt-4
                bg-blue-600
                hover:bg-blue-700
                text-white
                px-4
                py-2
                rounded-lg
                "
                >

                Jump To Moment

                </button>

              <div className="mt-2">

                {moment.sources.map(
                  source => (

                    <span
                      key={source}
                      className="
                      inline-block
                      bg-blue-100
                      text-blue-700
                      px-2
                      py-1
                      rounded
                      mr-2
                      "
                    >

                      {source}

                    </span>
                  )
                )}

              </div>

            </div>
          )
        )}

      </div>

    </div>
  );
}

export default MomentResults;