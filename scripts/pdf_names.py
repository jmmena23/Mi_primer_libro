PDF_FILENAMES = {
    "es": "FisiologiaRenal.pdf",
    "en": "RenalPhysiology.pdf",
}

# Default PDF filename (Spanish primary)
DEFAULT_PDF_FILENAME = PDF_FILENAMES["es"]

def pdf_filename_for_lang(lang: str) -> str:
    """Return the PDF filename for the given language code.

    Falls back to the default (Spanish) if the language is not recognized.
    """
    return PDF_FILENAMES.get(lang, DEFAULT_PDF_FILENAME)
