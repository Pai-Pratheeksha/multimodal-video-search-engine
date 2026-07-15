import { useState } from "react";
import { api } from "../api/api";

interface Props {

    onUploadSuccess:
      (videoName: string) => void;
}

function UploadForm({
  onUploadSuccess
}: Props) {

  const [files, setFiles] =
    useState<File[]>([]);

  const [message, setMessage] =
    useState("");

  const [messageType, setMessageType] =
    useState<"success" | "error">("success");

  const [uploading, setUploading] =
    useState(false);

  const handleUpload = async () => {

    if (files.length==0) {

      setMessage(
        "Please select a video."
      );

      return;
    }

    const formData =
      new FormData();

    files.forEach(file => {

        formData.append(
            "files",
            file
        );

    });

    try {

      setUploading(true);
      setMessage("");

      const response =
        await api.post(
          "/upload-batch",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data",
            },
          }
        );

      setMessageType("success");

      setMessage(
          response.data.message
      );

      if (response.data.processed.length > 0) {

          const latest =

              response.data.processed.at(-1);

          onUploadSuccess(

              latest.video_name

          );

      }

      setFiles([]);

    } catch (error: any) {

      console.error(error);

      if (error.response?.status === 409) {

        setMessageType("error");

        setMessage(
            "⚠️ This video has already been indexed."
        );

      } else {

          setMessageType("error");

          setMessage(
              "Failed to upload video."
          );

      }

    } finally {

      setUploading(false);

    }
  };

  const removeFile = (
      fileName: string
  ) => {

      const updatedFiles = files.filter(

          file => file.name !== fileName

      );

      setFiles(updatedFiles);

  };

  return (

    <div className="bg-white rounded-2xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-2">
        Upload Videos
      </h2>

      <p className="text-gray-500 mb-6">
        Upload MP4 videos for indexing,
        object detection and semantic search.
      </p>

      <label
        htmlFor={uploading ? undefined : "video-upload"}
        className={`
          flex
          flex-col
          items-center
          justify-center
          w-full
          h-40
          border-2
          border-dashed
          rounded-2xl
          transition

          ${
              uploading
              ? "bg-gray-100 border-gray-200 cursor-not-allowed"
              : "bg-gray-50 border-gray-300 hover:bg-gray-100 cursor-pointer"
          }
      `}
      >

        <div className="text-center">

          <div className="text-5xl mb-2">
            📹
          </div>

          <p className="font-semibold">
            Click to choose videos
          </p>

          <p className="text-sm text-gray-500 mt-1">
            MP4 files supported
          </p>

        </div>

      </label>

      <input
        multiple
        disabled={uploading}
        id="video-upload"
        type="file"
        accept=".mp4"
        className="hidden"
        onChange={(e) => {

          const selectedFiles =
              Array.from(
                  e.target.files || []
              );

          setFiles(prev => {

              const merged = [

                  ...prev,

                  ...selectedFiles

              ];

              return merged.filter(

                  (file, index, self) =>

                      index === self.findIndex(

                          f => f.name === file.name

                      )

              );

          });
        }}
      />

      {files.length > 0 && (

          <div
              className="
              mt-4
              p-4
              rounded-xl
              bg-blue-50
              border
              border-blue-200
              "
          >

              <p className="font-semibold mb-3">

                  Selected Videos ({files.length})

              </p>

              {

                  files.map(file => (

                      <div

                          key={file.name}

                          className="
                          flex
                          justify-between
                          items-center
                          gap-4
                          mb-3
                          px-4
                          py-2
                          bg-white
                          rounded-lg
                          "
                      >
                        <div className="flex-1 min-w-0">

                          <p className="font-medium truncate">

                              📹 {file.name}

                          </p>

                          <p className="text-sm text-gray-600">

                              {(file.size / 1024 / 1024).toFixed(2)} MB

                          </p>

                      </div>

                      <button

                          onClick={() =>

                              removeFile(file.name)

                          }

                          disabled={uploading}
                          className={`
                              flex-shrink-0
                              font-medium

                              ${
                                  uploading
                                  ? "text-gray-400 cursor-not-allowed"
                                  : "text-red-600 hover:text-red-800"
                              }
                          `}
                      >

                          🗑 Remove

                      </button>

                  </div>

                  ))

              }

          </div>

      )}

      <div className="flex gap-3 mt-5">

          {files.length > 0 && (

              <button

                  onClick={() => {

                      setFiles([]);

                  }}
                  disabled={uploading}

                  className={`
                    border
                    px-4
                    py-3
                    rounded-xl

                    ${
                        uploading
                        ? "border-gray-300 text-gray-400 cursor-not-allowed"
                        : "border-red-500 text-red-600"
                    }
                `}

              >

                  Clear All

              </button>

          )}

          <button

              onClick={handleUpload}

              disabled={
                  uploading ||
                  files.length === 0
              }

              className="
              flex-1
              bg-blue-600
              hover:bg-blue-700
              disabled:bg-gray-400
              text-white
              py-3
              rounded-xl
              font-medium
              transition
              "

          >

              {uploading

                  ? "Processing Videos..."

                  : "Upload Videos"

              }

          </button>

      </div>


      {uploading && (

          <p className="mt-3 text-sm text-blue-600">

              Please wait. Videos are being indexed.
              Do not close this page.

          </p>

      )}

      {message && (

        <div
            className={`

            mt-4
            p-3
            rounded-lg
            font-medium

            ${
                messageType === "success"

                ? "bg-green-50 border border-green-200 text-green-700"

                : "bg-red-50 border border-red-200 text-red-700"

            }

            `}
        >

            {message}

        </div>

    )}

    </div>
  );
}

export default UploadForm;
