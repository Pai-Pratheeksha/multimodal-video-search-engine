import { useEffect, useState, useRef } from "react";

import UploadForm from "../components/UploadForm";
import SearchBar from "../components/SearchBar";
import MomentResults from "../components/MomentResults";

import { api } from "../api/api";

import type { Moment } from "../types/moment";

import VideoPlayer
from "../components/VideoPlayer";

function Home() {

  const [results, setResults] =
    useState<Moment[] | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [backendStatus, setBackendStatus] =
    useState("Checking...");

  const [previewUrl, setPreviewUrl] =
    useState<string | null>(null);

  const [activeTimestamp, setActiveTimestamp] =
    useState<number | null>(null);

  const [videoReady, setVideoReady] =
    useState(false);

  const [videoName, setVideoName] =
    useState("");

  const videoRef =
    useRef<HTMLVideoElement>(null);

  const videoContainerRef =
    useRef<HTMLDivElement>(null);

  const checkVideoStatus = async () => {

        try {

          const response =
            await api.get(
              "/video-status"
            );

          setVideoReady(
            response.data.video_ready
          );

          setVideoName(
            response.data.video_name || ""
          );

          if (
            response.data.video_url
          ) {

            setPreviewUrl(
              response.data.video_url
            );
          }

        } catch {

          setVideoReady(false);

        }
    };

  useEffect(() => {

    const checkBackend = async () => {

        try {

        await api.get("/health");

        setBackendStatus(
            "Online"
        );

        } catch {

        setBackendStatus(
            "Offline"
        );

        }

    };

    checkBackend();

    checkVideoStatus();

    const interval =
        setInterval(
        checkBackend,
        10000
        );

    return () =>
        clearInterval(interval);
    }, []);

  const handleSearch = async (
    query: string
  ) => {

    setLoading(true);

    try {

      const response =
        await api.get<Moment[]>(
          `/multimodal-search?query=${query}`
        );

      setResults(
        response.data
      );

    } catch (error: any) {

      console.error(error);

      alert(
        error.response?.data?.detail ||
        "Search failed."
      );

      setBackendStatus(
        "Offline"
      );

    } finally {

      setLoading(false);

    }
  };

  const jumpToMoment = (
    timestamp: number
  ) => {

    setActiveTimestamp(
      timestamp
    );

    videoContainerRef.current
      ?.scrollIntoView({

        behavior: "smooth",

        block: "start"
    });

    const video =
      videoRef.current;

    if (!video) {
      return;
    }

    video.currentTime =
      timestamp;

    const handleSeeked =
      async () => {

        video.removeEventListener(
          "seeked",
          handleSeeked
        );

        try {

          await video.play();

        } catch (error) {

          console.error(
            "Playback failed:",
            error
          );

        }
      };

    video.addEventListener(
      "seeked",
      handleSeeked
    );
  };

  console.log(previewUrl);

  return (

    <div className="min-h-screen bg-slate-100">

      <div className="max-w-6xl mx-auto px-6 py-10">

        {/* HEADER */}

        <div className="bg-white rounded-3xl shadow-lg p-10 mb-8">

          <h1 className="text-5xl font-bold text-center text-slate-800">

            Multimodal Video Search Engine

          </h1>

          <p className="text-center text-slate-500 mt-4 text-lg">

            Semantic Video Retrieval using
            CLIP • YOLO • Whisper • FAISS

          </p>

        </div>

        {/* STATUS BAR */}

        <div className="bg-white rounded-2xl shadow p-4 mb-8 flex justify-between items-center">

          <div>

            <h2 className="font-semibold text-lg">
              System Status
            </h2>

            <p className="text-gray-500 text-sm">
              FastAPI Backend Connection
            </p>

          </div>

          <div className="flex items-center gap-2">

            <div
                className={`w-3 h-3 rounded-full ${
                    backendStatus === "Online"
                    ? "bg-green-500"
                    : backendStatus === "Offline"
                    ? "bg-red-500"
                    : "bg-yellow-500"
                }`}
                ></div>

                <span
                className={`font-medium ${
                    backendStatus === "Online"
                    ? "text-green-700"
                    : backendStatus === "Offline"
                    ? "text-red-700"
                    : "text-yellow-700"
                }`}
                >
                {backendStatus}
                </span>

          </div>

        </div>

        <div className="
          bg-white
          rounded-2xl
          shadow
          p-4
          mb-8
          ">

            <h2 className="
            font-semibold
            text-lg
            ">

              Indexed Video

            </h2>

            {videoReady ? (

              <p className="
              text-green-700
              mt-2
              ">

                📹 {videoName}

              </p>

            ) : (

              <p className="
              text-red-600
              mt-2
              ">

                No video uploaded

              </p>

            )}

          </div>

        {/* UPLOAD SECTION */}

        <div className="mb-8">

          <UploadForm
            setPreviewUrl={setPreviewUrl}
            onUploadSuccess={checkVideoStatus}
          />

        </div>

        <div ref={videoContainerRef}>

          <VideoPlayer
            ref={videoRef}
            videoUrl={previewUrl}
          />

        </div>

        {/* SEARCH SECTION */}

        <div className="mb-8">

          <SearchBar
            onSearch={handleSearch}
            disabled={!videoReady}
          />

        </div>

        {/* LOADING */}

        {loading && (

          <div className="bg-white rounded-2xl shadow p-6 mb-8">

            <div className="flex items-center gap-4">

              <div className="w-5 h-5 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>

              <p className="font-medium">

                Searching video content...

              </p>

            </div>

          </div>

        )}

        {/* RESULTS */}

        {results && results.length > 0 && !loading && (

          <div className="bg-white rounded-3xl shadow-lg p-8">

            <h2 className="text-3xl font-bold mb-6 text-slate-800">

              Multimodal Search Results

            </h2>

            <MomentResults
              results={results}
              onJump={jumpToMoment}
              activeTimestamp={
                activeTimestamp
              }
            />

          </div>

        )}

        {results &&
          results.length === 0 &&
          !loading && (

            <div className="
            bg-white
            rounded-3xl
            shadow-lg
            p-10
            text-center
            ">

              <div className="text-6xl mb-4">
                🔍
              </div>

              <h2 className="
              text-2xl
              font-bold
              text-slate-700
              mb-2
              ">
                No Results Found
              </h2>

              <p className="text-slate-500">
                Try a different search query.
              </p>

            </div>

          )}

      </div>

    </div>
  );
}

export default Home;