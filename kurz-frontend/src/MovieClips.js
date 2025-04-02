import React, { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

const movies = [
  { title: "Inception", clip: "/videos/inception.mp4" },
  { title: "Interstellar", clip: "/videos/inception.mp4" },
  { title: "The Matrix", clip: "/videos/inception.mp4" },
  { title: "The Dark Knight", clip: "/videos/inception.mp4" },
];

const MovieClips = () => {
  const videoRefs = useRef([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const video = entry.target;
          // Only play the video when it's 50% visible
          if (entry.isIntersecting) {
            // Pause all other videos before playing the current one
            videoRefs.current.forEach((vid) => {
              if (vid !== video) {
                vid.pause();
                vid.currentTime = 0; // Reset the video time to the start
              }
            });
            // Play the current video
            video.play().catch((error) => {
              // Handle any error (e.g., autoplay blocked by the browser)
              console.error("Play error: ", error);
            });
          } else {
            // Pause the video when it's not visible
            video.pause();
          }
        });
      },
      {
        threshold: 0.5, // Play video when 50% visible
      }
    );

    videoRefs.current.forEach((video) => {
      if (video) observer.observe(video);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        height: "100vh",
        overflowY: "auto",
        p: 3,
        gap: 3,
      }}
    >
      <Typography variant="h6" align="center" sx={{ mb: 2 }}>
        Kurz
      </Typography>
      {movies.map((movie, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card sx={{ width: 470, boxShadow: 3, borderRadius: 2 }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" align="center" sx={{ mb: 2 }}>
                {movie.title}
              </Typography>
              <Box display="flex" justifyContent="center">
                <video
                  ref={(el) => (videoRefs.current[index] = el)}
                  src={movie.clip}
                  muted
                  loop
                  playsInline
                  style={{
                    width: "980px", // Increased size
                    height: "470px", // Increased size
                    objectFit: "cover",
                    borderRadius: "8px",
                  }}
                ></video>
              </Box>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </Box>
  );
};

export default MovieClips;
