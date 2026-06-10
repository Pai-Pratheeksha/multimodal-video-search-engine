import { forwardRef } from "react";

interface Props {

  videoUrl: string | null;
}

const VideoPlayer = forwardRef<
  HTMLVideoElement,
  Props
>(
  ({ videoUrl }, ref) => {

    if (!videoUrl) {

      return null;
    }

    return (

      <div className="
      bg-white
      rounded-2xl
      shadow-lg
      p-6
      mb-8
      ">

        <h2 className="
        text-2xl
        font-bold
        mb-4
        ">

          Video Preview

        </h2>

        <video
        key={videoUrl}
        ref={ref}
        controls
          className="
          w-full
          rounded-xl
          border
          "
        >

          <source
            src={videoUrl}
            type="video/mp4"
          />

        </video>

      </div>
    );
  }
);

export default VideoPlayer;