import { useState } from "react";
import { api } from "../api/api";

interface Props {

  setPreviewUrl:
    React.Dispatch<
      React.SetStateAction<
        string | null
      >
    >;

    onUploadSuccess:
      (videoName: string) => void;
}

function UploadForm({
  setPreviewUrl,
  onUploadSuccess
}: Props) {

  const [file, setFile] =
    useState<File | null>(null);

  const [message, setMessage] =
    useState("");

  const [messageType, setMessageType] =
    useState<"success" | "error">("success");

  const [uploading, setUploading] =
    useState(false);

  const handleUpload = async () => {

    if (!file) {

      setMessage(
        "Please select a video."
      );

      return;
    }

    const formData =
      new FormData();

    formData.append(
      "file",
      file
    );

    try {

      setUploading(true);
      setMessage("");

      const response =
        await api.post(
          "/upload",
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

      onUploadSuccess(response.data.filename);

      setPreviewUrl(
        `http://127.0.0.1:8000/videos/${response.data.filename}`
      );

      setFile(null);

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

  return (

    <div className="bg-white rounded-2xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-2">
        Upload Video
      </h2>

      <p className="text-gray-500 mb-6">
        Upload an MP4 video for indexing,
        object detection and semantic search.
      </p>

      <label
        htmlFor="video-upload"
        className="
        flex
        flex-col
        items-center
        justify-center
        w-full
        h-40
        border-2
        border-dashed
        border-gray-300
        rounded-2xl
        bg-gray-50
        hover:bg-gray-100
        cursor-pointer
        transition
        "
      >

        <div className="text-center">

          <div className="text-5xl mb-2">
            📹
          </div>

          <p className="font-semibold">
            Click to choose a video
          </p>

          <p className="text-sm text-gray-500 mt-1">
            MP4 files supported
          </p>

        </div>

      </label>

      <input
        id="video-upload"
        type="file"
        accept=".mp4"
        className="hidden"
        onChange={(e) => {

          const selectedFile =
            e.target.files?.[0] || null;

          setFile(
            selectedFile
          );

          if (selectedFile) {
            setPreviewUrl(
                URL.createObjectURL(
                    selectedFile
                )
            );}
        }}
      />

      {file && (

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

          <p className="font-semibold">
            {file.name}
          </p>

          <p className="text-sm text-gray-600">

            Size:
            {" "}
            {(file.size / 1024 / 1024)
              .toFixed(2)}
            {" "}
            MB

          </p>

        </div>

      )}

      <button
        onClick={handleUpload}
        disabled={uploading}
        className="
        mt-6
        bg-blue-600
        hover:bg-blue-700
        disabled:bg-gray-400
        text-white
        px-6
        py-3
        rounded-xl
        font-medium
        transition
        "
      >

        {uploading
          ? "Processing Video..."
          : "Upload Video"}

      </button>

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
