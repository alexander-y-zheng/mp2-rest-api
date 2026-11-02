import logging

logger = logging.getLogger(__name__)


class DatasetStorage:
    def __init__(self):
        self._store = {}
        self._counter = 0

    def save(self, df, filename):
        """Store a copy of the data and return a new integer ID."""
        self._counter += 1
        dataset_id = self._counter
        self._store[dataset_id] = {
            "df": df.copy(),
            "filename": filename
        }
        logger.debug("Stored dataset: id=%s, rows=%s", dataset_id, len(df))
        return dataset_id

    def get(self, dataset_id):
        """Return a copy of the stored DataFrame, or None."""
        if dataset_id in self._store:
            df = self._store[dataset_id]["df"].copy()
            logger.debug("Retrieved dataset copy: id=%s, rows=%s", dataset_id, len(df))
            return df
        logger.debug("Dataset not found: id=%s", dataset_id)
        return None

    def get_metadata(self, dataset_id):
        """Return the dataset metadata, or None."""
        if dataset_id in self._store:
            df = self._store[dataset_id]["df"]
            return {
                "id": dataset_id,
                "filename": self._store[dataset_id]["filename"],
                "rows": df.shape[0],
                "columns": df.shape[1],
                "column_names": list(df.columns)
            }
        logger.debug("Metadata requested for missing dataset: id=%s", dataset_id)
        return None

    def update(self, dataset_id, df):
        """Replace an existing dataset; return True, or False if missing."""
        if dataset_id in self._store:
            self._store[dataset_id]["df"] = df.copy()
            logger.debug("Updated dataset: id=%s, rows=%s", dataset_id, len(df))
            return True
        logger.debug("Cannot update missing dataset: id=%s", dataset_id)
        return False

    def clear(self):
        """Clear all data and reset the ID counter."""
        logger.debug("Clearing dataset storage: datasets=%s", len(self._store))
        self._store.clear()
        self._counter = 0
