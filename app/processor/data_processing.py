import logging
import os
import sqlite3
import time
from datetime import datetime

from app.models.record import Records
from app.services.database import SessionLocal
from app.utils.consts import LOG_LENGTH, BATCH_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Setup SQLite database and table
def setup_database():
    try:
        conn = sqlite3.connect("api_requests.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                customer_id TEXT,
                request_path TEXT,
                status_code INTEGER,
                duration REAL
            )
        """
        )
        conn.commit()
        return conn, cursor
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        return False


# Parse log file and insert data into database
# Parse log file and insert data into database in batches
def process_log_file(file_path: str, batch_size: int = BATCH_SIZE) -> bool:
    """
    Parse the log file and insert data into the database in batches.

    Args:
        file_path (str): Path to the log file.
        batch_size (int, optional): Number of records to process in each batch. Defaults to BATCH_SIZE.

    Returns:
        bool: True if processing is successful, False otherwise.
    """
    if not os.path.exists(file_path):
        logger.error(f"Log file not found: {file_path}")
        return False

    try:
        with SessionLocal() as session:
            with open(file_path, "r") as file:
                batch = []
                for line in file:
                    try:
                        parts = line.strip().split()
                        if len(parts) != LOG_LENGTH:
                            raise ValueError(f"Incorrect log format: {line.strip()}")
                        # Extract parts
                        (
                            data_str,
                            time_str,
                            customer_id,
                            request_path,
                            status_code,
                            duration,
                        ) = parts

                        # Parse timestamp
                        timestamp = datetime.strptime(
                            data_str + " " + time_str, "%Y-%m-%d %H:%M:%S"
                        )

                        # Create record object
                        record = Records(
                            timestamp=timestamp,
                            customer_id=customer_id,
                            request_path=request_path,
                            status_code=int(status_code),
                            duration=float(duration),
                        )
                        batch.append(record)

                        # Commit batch if batch size is reached
                        if len(batch) >= batch_size:
                            session.bulk_save_objects(batch)
                            session.commit()
                            batch = []

                    except ValueError as ve:
                        logger.warning(f"Error processing line: {ve}")

                    except Exception as e:
                        logger.error(f"Unexpected error: {e}")

                # Commit any remaining records in the batch
                if batch:
                    session.bulk_save_objects(batch)
                    session.commit()

        return True

    except Exception as e:
        logger.error(f"Error processing log file: {e}")
        return False


# Main function
def main():
    """
    Main function to set up the database and process the log file.
    """
    conn, cursor = setup_database()
    process_log_file("../../api_requests.log")
    conn.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("execution time", start_time - end_time)
