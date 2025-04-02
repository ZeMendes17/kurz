import React, { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { IconButton, Button } from "@mui/material";
import FavoriteIcon from "@mui/icons-material/Favorite";
import MovieIcon from "@mui/icons-material/Movie";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import { useParams, useNavigate } from "react-router-dom";

// Full movie data array with correct structure
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
    clip: "/videos/star_wars.mp4",
    tags: ["adventure", "action", "science fiction"],
  },
  {
    id: "tt0114148",
    title: "Pocahontas",
    clip: "/videos/pocahontas.mp4",
    tags: ["adventure", "action", "science fiction"],
  },
];

// Order of IDs for navigation
const ids = [
  "tt0114148",
  "tt0076759",
  "tt0113189",
  "tt0065421",
  "tt0112442",
  "tt0120783",
  "tt0117008",
  "tt0067992",
  "tt0109830",
  "tt0114709",
  "tt0055277"
];

const MovieClip = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const [currentMovie, setCurrentMovie] = useState(null);

  const addToFavourite = async (id) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/like/${id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: null,
        }
      );

      const data = await response.json();
      console.log("Added to favorites:", data);
    } catch (error) {
      console.error("Error adding to favorites:", error);
    }
  };

  const goToNext = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/recommendation",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();

      console.log("Got ID:", data["movie"]);
      const foundMovie = movies.find(
        (movie) => movie.id === data["movie"]["imdb_id"]
      );
      if (foundMovie) {
        setCurrentMovie(foundMovie);
      } else {
        console.error("Movie not found in the list");
        return;
      }
      navigate(`/movie/${data["movie"]["imdb_id"]}`);
    } catch (error) {
      console.error("Error adding to favorites:", error);
    }
  };

  //  Find movie details based on ID parameter
  useEffect(() => {
    // Find the movie with the matching ID
    const foundMovie = movies.find((movie) => movie.id === id);

    if (foundMovie) {
      setCurrentMovie(foundMovie);
    } else {
      // If no match, use the first movie in the ids array
      const firstId = ids[0];
      const defaultMovie = movies.find((movie) => movie.id === firstId);
      setCurrentMovie(defaultMovie);

      // Update URL to match the actual movie being shown
      navigate(`/movie/${firstId}`, { replace: true });
    }
  }, [id, navigate]);

  // Handle video playback when the movie changes
  useEffect(() => {
    if (videoRef.current && currentMovie) {
      videoRef.current.currentTime = 0;
      videoRef.current.play().catch((error) => {
        console.error("Play error: ", error);
      });
    }

    return () => {
      if (videoRef.current) {
        videoRef.current.pause();
      }
    };
  }, [currentMovie]);

  // Navigation function
  const navigateToMovie = (direction) => {
    if (!currentMovie) return;

    const currentIdIndex = ids.indexOf(currentMovie.id);
    let nextIdIndex;

    if (direction === "next") {
      nextIdIndex = (currentIdIndex + 1) % ids.length;
    } else {
      nextIdIndex = (currentIdIndex - 1 + ids.length) % ids.length;
    }

    navigate(`/movie/${ids[nextIdIndex]}`);
  };

  if (!currentMovie) return <Box sx={{ color: "#fff" }}>Loading...</Box>;

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        height: "100vh",
        p: 3,
        backgroundColor: "#000",
      }}
    >
      <Typography
        variant="h4"
        align="center"
        sx={{ mb: 4, color: "#fff", font: "Poppins" }}
      >
        Kurz Vid
      </Typography>

      <motion.div
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
                ref={videoRef}
                src={currentMovie.clip}
                loop
                muted
                playsInline
                style={{
                  width: "960px",
                  height: "544px",
                  objectFit: "cover",
                  borderRadius: "8px",
                }}
              />
            </Box>
            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-between",
              }}
            >
              <Box
                sx={{
                  alignContent: "center",
                }}
              >
                <Button
                  startIcon={<ArrowBackIcon />}
                  variant="contained"
                  onClick={() => navigateToMovie("prev")}
                  sx={{
                    backgroundColor: "#333",
                    "&:hover": { backgroundColor: "#555" },
                  }}
                >
                  Previous
                </Button>
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
                  {currentMovie.title}
                </Typography>
                <Typography variant="body2" sx={{ color: "#bbb" }}>
                  {currentMovie.tags.map((tag, index) => `#${tag} `)}
                </Typography>
              </Box>

              <Box
                sx={{
                  alignContent: "center",
                }}
              >
                <Button
                  endIcon={<ArrowForwardIcon />}
                  variant="contained"
                  onClick={() => {
                    //navigateToMovie("next");
                    goToNext();
                  }}
                  sx={{
                    backgroundColor: "#333",
                    "&:hover": { backgroundColor: "#555" },
                  }}
                >
                  Next
                </Button>
              </Box>
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
          <IconButton
            sx={{ color: "#fff" }}
            onClick={() => {
              addToFavourite(currentMovie.id);
            }}
          >
            <FavoriteIcon />
          </IconButton>
          <IconButton
            sx={{ color: "#fff" }}
            onClick={() => {
              window.open(`https://www.imdb.com/title/${currentMovie.id}/`);
            }}
          >
            <MovieIcon />
          </IconButton>
        </Box>
      </motion.div>
    </Box>
  );
};

export default MovieClip;
