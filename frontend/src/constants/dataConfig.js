export const DATA_CONFIG = {
  STANDARD_COLUMN_ORDER: ["Title", "Price", "Metadata", "Text", "Link", "Image"],
  HIGHLIGHT_COLUMNS: {
    PRIMARY: ["Title", "Price"],
    BOLD: ["Metadata"],
    LINK: ["Link"],
    TEXT_MUTED: ["Image"]
  },
  EXPORT: {
    CSV_MIME_HEADER: "data:text/csv;charset=utf-8,",
    CSV_FILENAME: "quantana_extract.csv",
    JSON_MIME_HEADER: "data:text/json;charset=utf-8,",
    JSON_FILENAME: "quantana_extract.json",
    JSON_INDENT_SPACES: 2
  }
};
