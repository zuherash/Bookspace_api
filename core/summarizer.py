from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import nltk


def _ensure_tokenizers() -> None:
    """Download required NLTK tokenizers if they are missing."""
    for pkg in ["punkt", "punkt_tab"]:
        try:
            nltk.data.find(f"tokenizers/{pkg}")
        except LookupError:  # pragma: no cover - network access may fail
            try:
                nltk.download(pkg, quiet=True)
            except Exception:
                pass


def summarize_text(text: str, sentence_count: int = 3) -> str:
    _ensure_tokenizers()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)
