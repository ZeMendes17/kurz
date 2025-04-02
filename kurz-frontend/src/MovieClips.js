import React, { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { IconButton } from "@mui/material";
import FavoriteIcon from "@mui/icons-material/Favorite";
import MovieIcon from "@mui/icons-material/Movie";

const movies = [
  {
    id: "tt0114709",
    title: "Toy Story",
    clip: "/videos/toy_story.mp4",
    tags: ["comedy", "animation", "family"],
  },
  {
    id: "tt0109830",
    title: "Forrest Gump",
    clip: "/videos/forrest_gump.mp4",
    tags: ["comedy", "drama", "romance"],
  },
  {
    id: "tt0067992",
    title: "Willy Wonka and The Chocolate Factory",
    clip: "/videos/willy_wonka.mp4",
    tags: ["family", "fantasy"],
  },
  {
    id: "tt0117008",
    title: "Matilda",
    clip: "/videos/matilda.mp4",
    tags: ["comedy", "fantasy", "family"],
  },
  {
    id: "tt0120783",
    title: "The Parent Trap",
    clip: "/videos/the_parent_trap.mp4",
    tags: ["comedy", "family"],
  },
  {
    id: "tt0112442",
    title: "Bad Boys",
    clip: "/videos/bad_boys.mp4",
    tags: ["adventure", "action", "science fiction"],
  },
  {
    id: "tt0065421",
    title: "Aristocats",
    clip: "/videos/aristocats.mp4",
    tags: ["adventure", "action", "science fiction"],
  },
  {
    id: "tt0113189",
    title: "Golden Eye",
    clip: "/videos/golden_eye.mp4",
    tags: ["adventure", "action", "science fiction"],
  },
  {
    id: "tt0076759",
    title: "Star Wars: A New Hope (Episode IV)",
    clip: "/videos/golden_eye.mp4",
    tags: ["adventure", "action", "science fiction"],
  },
  {
    id: "tt0114148",
    title: "Pocahontas",
    clip: "/videos/pocahontas.mp4",
    tags: ["adventure", "action", "science fiction"],
  },
];

const MovieClips = () => {
  const videoRefs = useRef([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const video = entry.target;
          if (entry.isIntersecting) {
            videoRefs.current.forEach((vid) => {
              if (vid !== video) {
                vid.pause();
                vid.currentTime = 0;
              }
            });
            video.play().catch((error) => {
              console.error("Play error: ", error);
            });
          } else {
            video.pause();
          }
        });
      },
      { threshold: 0.5 }
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
        backgroundColor: "#000",
      }}
    >
      <Typography variant="h4" align="center" sx={{ mb: 2, color: "#fff" }}>
        Kurz Vid
      </Typography>
      {movies.map((movie, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{ position: "relative", display: "flex" }}
        >
          <Card
            sx={{
              width: 960,
              boxShadow: 3,
              borderRadius: 2,
              backgroundColor: "#000",
            }}
          >
            <CardContent>
              <Box
                display="flex"
                justifyContent="center"
                sx={{ backgroundColor: "#000" }}
              >
                <video
                  ref={(el) => (videoRefs.current[index] = el)}
                  src={movie.clip}
                  loop
                  muted
                  playsInline
                  style={{
                    width: "960px",
                    height: "544px",
                    objectFit: "cover",
                    borderRadius: "8px",
                  }}
                ></video>
              </Box>

              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  mt: 2,
                  p: 1,
                  backgroundColor: "rgba(0, 0, 0, 0.7)",
                  borderRadius: "8px",
                }}
              >
                <Typography
                  variant="h6"
                  sx={{ fontWeight: "bold", color: "#fff" }}
                >
                  {movie.title}
                </Typography>
                <Typography variant="body2" sx={{ color: "#bbb" }}>
                  {movie.tags.map((tag, index) => `#${tag} `)}
                </Typography>
              </Box>
            </CardContent>
          </Card>

          <Box
            sx={{
              position: "absolute",
              right: -70,
              top: "50%",
              transform: "translateY(-50%)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 2,
              background: "#333",
              padding: "10px",
              borderRadius: "12px",
            }}
          >
            <IconButton sx={{ color: "#fff" }}>
              <FavoriteIcon />
            </IconButton>
            <IconButton
              sx={{ color: "#fff" }}
              onClick={() => {
                window.open(`https://www.imdb.com/title/${movie.id}/`);
              }}
            >
              <MovieIcon />
            </IconButton>
          </Box>
        </motion.div>
      ))}
    </Box>
  );
};

export default MovieClips;
