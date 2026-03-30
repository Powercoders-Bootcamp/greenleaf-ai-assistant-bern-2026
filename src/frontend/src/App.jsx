import { useState } from "react";
import PropTypes from "prop-types";
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from "motion/react";
import "./App.css";

// Import the new brutalist logo
import logo from "./assets/logo.svg";

// Brutalist Heading - instant appear, no blur
function BrutalistHeading({ text }) {
  const words = text.split(" ");

  return (
    <h1 className="brutalist-heading" aria-label={text}>
      {words.map((word, wordIndex) => (
        <span className="brutalist-word" key={`${word}-${wordIndex}`}>
          {word.split("").map((char, charIndex) => (
            <motion.span
              key={`${char}-${wordIndex}-${charIndex}`}
              className="brutalist-char"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{
                duration: 0.1,
                delay: wordIndex * 0.05 + charIndex * 0.01,
              }}
            >
              {char}
            </motion.span>
          ))}
        </span>
      ))}
    </h1>
  );
}
BrutalistHeading.propTypes = {
  text: PropTypes.string.isRequired,
};

// Sources Sidebar - replacing JellyWindow with a stark, static column
function SourcesWidget({ sources, visible }) {
  if (!visible) return null;

  return (
    <motion.aside
      className="sources-widget"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <div className="sources-widget__header">
        <p>SOURCES / WIDGET</p>
      </div>

      <div className="sources-widget__body">
        {sources.map((source, index) => (
          <motion.div
            key={`${source.title}-${index}`}
            className="source-block"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="source-block__meta">
              <span>{source.title}</span>
              <span className="confidence">{source.confidence}</span>
            </div>
            <p>{source.section}</p>
          </motion.div>
        ))}
      </div>
    </motion.aside>
  );
}
SourcesWidget.propTypes = {
  sources: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string.isRequired,
      confidence: PropTypes.string,
      section: PropTypes.string,
    })
  ).isRequired,
  visible: PropTypes.bool.isRequired,
};

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/ask";

  const handleAsk = async () => {
    if (!question.trim()) {
      setError("PLEASE ENTER A QUESTION.");
      setAnswer(null);
      setSources([]);
      return;
    }

    setLoading(true);
    setError("");
    setAnswer(null);
    setSources([]);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail?.[0]?.msg || data?.error || "REQUEST FAILED.");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message || "SOMETHING WENT WRONG. PLEASE CHECK YOUR BACKEND.");
    } finally {
      setLoading(false);
    }
  };

  const onKeyDown = (event) => {
    if (event.key === "Enter") handleAsk();
  };

  // Helper function to parse **bold** text from the backend
  // This turns **text** into a <strong> HTML element.
  const formatText = (text) => {
    if (!text) return null;
    const parts = text.split(/(\*\*.*?\*\*)/g);
    
    return parts.map((part, i) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={i} style={{ fontWeight: 800, textDecoration: 'underline' }}>
            {part.slice(2, -2)}
          </strong>
        );
      }
      return part;
    });
  };

  return (
    <main className="brutalist-layout">
      {/* Top Navigation / Branding */}
      <nav className="top-nav">
        <div>
          {/* Integrated the new SVG logo here */}
          <img src={logo} alt="GreenLeaf Logo" style={{ height: '40px' }} />
        </div>
        <div style={{ alignSelf: 'center' }}>BERN GROUP / 2026</div>
      </nav>

      <div className="grid-container">
        {/* Left Column: Interaction */}
        <section className="interaction-column">
          <header className="header-block">
            <BrutalistHeading text="ASK THE HANDBOOK" />
            <p className="subtitle">
              ENTER YOUR POLICY QUESTION BELOW. THE ASSISTANT WILL RETRIEVE TRUSTED ANSWERS FROM THE DATABASE.
            </p>
          </header>

          <div className="form-group">
            <label htmlFor="question-input">QUERY INPUT</label>
            <input
              id="question-input"
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value.toUpperCase())}
              onKeyDown={onKeyDown}
              placeholder="START TYPING YOUR QUESTION..."
              className="brutalist-input"
              autoComplete="off"
            />
            
            <button
              className="brutalist-button"
              onClick={handleAsk}
              disabled={loading || !question.trim()}
            >
              {loading ? "PROCESSING..." : "SUBMIT QUERY"}
            </button>
          </div>

          <div className="response-area">
            <AnimatePresence mode="wait">
              {error && (
                <motion.div
                  key="error"
                  className="response-block is-error"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <label>SYSTEM ERROR</label>
                  <p>{error}</p>
                </motion.div>
              )}

              {loading && (
                <motion.div
                  key="loading"
                  className="response-block is-loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <label>STATUS</label>
                  <p>RETRIEVING DATA...</p>
                </motion.div>
              )}

              {answer && !loading && !error && (
                <motion.div
                  key="answer"
                  className="response-block is-success"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <label>OUTPUT</label>
                  {/* Applied the formatting function here */}
                  <p>{formatText(answer)}</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </section>

        {/* Right Column: Sources / Empty State */}
        <section className="summary-column">
          {sources.length > 0 ? (
            <SourcesWidget sources={sources} visible={sources.length > 0} />
          ) : (
            <div className="empty-cart-style">
              <p>NO SOURCES LOADED</p>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

export default App;