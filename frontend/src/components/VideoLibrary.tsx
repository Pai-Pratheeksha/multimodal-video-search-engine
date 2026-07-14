import { useEffect, useState } from "react";
import { getVideos } from "../api/api";

interface Video {

    video_id: string;

    video_name: string;

}

interface Props {
    refreshKey: number;
    selectedVideo: string | null;
    selectedVideos: string[];

    setSelectedVideos:
        React.Dispatch<
            React.SetStateAction<string[]>
        >;
    onPreview: (videoName: string) => void;
}

function VideoLibrary({
    refreshKey,
    selectedVideo,
    selectedVideos,
    setSelectedVideos,
    onPreview

}: Props) {

    const [videos, setVideos] =
        useState<Video[]>([]);

    const [loading, setLoading] =
        useState(true);

    useEffect(() => {

        loadVideos();

    }, [refreshKey]);

    const loadVideos = async () => {
        setLoading(true);
        try {

            const response =
                await getVideos();

            setVideos(
                response.data
            );

        } catch (error) {

            console.error(
                error
            );

            setVideos([]);

        } finally {

            setLoading(false);

        }

    };

    if (loading) {

        return (

            <div className="bg-white rounded-2xl shadow p-6">

                <h2 className="text-2xl font-bold mb-4">

                    Indexed Videos

                </h2>

                <p className="text-gray-500">

                    Loading indexed videos...

                </p>

            </div>

        );

    }

    const toggleVideoSelection = (
        videoId: string
    ) => {

        setSelectedVideos(prev =>

            prev.includes(videoId)

            ? prev.filter(
                id => id !== videoId
            )

            : [...prev, videoId]

        );

    };

    return (

        <div className="bg-white rounded-2xl shadow p-6">

            <h2 className="text-2xl font-bold mb-4">

                Indexed Videos ({videos.length})

            </h2>

            {

                videos.length === 0 ?

                (

                    <div className="text-center py-10">

                        <div className="text-5xl mb-4">

                            📂

                        </div>

                        <p className="font-semibold text-lg">

                            No videos indexed yet

                        </p>

                        <p className="text-gray-500 mt-2">

                            Upload your first video to start searching.

                        </p>

                    </div>

                )

                :

                videos.map(video => (

                    <div

                        key={video.video_id}

                        className={`
                            flex
                            justify-between
                            items-center
                            rounded-lg
                            p-3
                            mb-3
                            border

                            ${
                                selectedVideo === video.video_name

                                ? "border-blue-500 bg-blue-50"

                                : "border-gray-200"

                            }
                        `}

                    >

                        <div className="flex items-center gap-3">

                            <input
                                type="checkbox"
                                className="w-5 h-5 accent-blue-600 cursor-pointer"
                                checked={selectedVideos.includes(video.video_id)}
                                onChange={() => toggleVideoSelection(video.video_id)}
                            />

                            <div>

                                <p className="font-medium">

                                    📹 {video.video_name}

                                </p>

                                {

                                    selectedVideo === video.video_name && (

                                        <p className="text-blue-600 text-sm">

                                            👁 Currently Playing

                                        </p>

                                    )

                                }

                            </div>

                        </div>

                        <div className="flex gap-2">

                        <button

                            onClick={() =>
                                onPreview(video.video_name)
                            }

                            className="
                            bg-blue-500
                            hover:bg-blue-600
                            text-white
                            px-4
                            py-2
                            rounded-lg
                            "
                        >

                            Play

                        </button>

                        <button

                            disabled

                            className="
                            bg-gray-300
                            text-gray-600
                            px-4
                            py-2
                            rounded-lg
                            cursor-not-allowed
                            "

                        >

                            🗑 Delete

                        </button>

                    </div>

                    </div>

                ))

            }

        </div>

    );

}

export default VideoLibrary;