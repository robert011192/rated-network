import datetime
from bytewax.dataflow import Dataflow
from bytewax.inputs import DynamicSource

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.record import Records
from app.core.config import settings

DATABASE_URL = settings.sql_alchemy_uri()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def input_builder(worker_index, worker_count):
    with open("api_requests.log", "r") as f:
        for line in f:
            yield line.strip()


def parse_line(line):
    parts = line.split()
    timestamp = datetime.datetime.strptime(
        parts[0] + " " + parts[1], "%Y-%m-%d %H:%M:%S"
    )
    customer_id = parts[2]
    request_path = parts[3]
    status_code = int(parts[4])
    duration = float(parts[5])
    return Records(
        timestamp=timestamp,
        customer_id=customer_id,
        request_path=request_path,
        status_code=status_code,
        duration=duration,
    )


def output_builder(session):
    def insert_request(request):
        session.add(request)
        session.commit()

    return insert_request


flow = Dataflow()

# Define the input using DynamicSource
flow.input("input", DynamicSource(input_builder))

flow.map(parse_line)


# Define a custom output function directly in the dataflow
def custom_output_builder(worker_index, worker_count):
    session = SessionLocal()
    insert_request = output_builder(session)
    return insert_request


flow.output("output", custom_output_builder)

if __name__ == "__main__":
    flow.run()
