import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getVideos = () =>
  api.get("/videos");

export const uploadVideo = (formData: FormData) =>
  api.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

export const searchVideos = (
  query: string,
  selectedVideos?: string[]
) =>
  api.get("/multimodal-search", {
    params: {
      query,
      ...(selectedVideos &&
        selectedVideos.length > 0 && {
          videos: selectedVideos.join(","),
        }),
    },
  });

export const getVideoStatus = () =>
  api.get("/video-status");

export const getVideoInfo = () =>
  api.get("/video-info");

export const deleteVideo = (
    videoId: string
) => {

    return api.delete(
        `/video/${videoId}`
    );

};