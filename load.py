from dagster import op, Out, In, get_dagster_logger
from sqlalchemy import create_engine, exc
from sqlalchemy.pool import NullPool
import pandas as pd

postgres_connection_string = "postgresql://dap:dap@127.0.0.1:5433/TeamA_HousingCrisis_Project"

@op(ins={'start': In(None)},out=Out(bool))
def load_immigration(start):
    logger = get_dagster_logger()
    immigration = pd.read_csv("staging/immigration.csv", sep="\t")
    try:
        engine = create_engine(postgres_connection_string,poolclass=NullPool)
        engine.execute("TRUNCATE immigration;")
        rowcount = immigration.to_sql(
            name="immigration",
            schema="public",
            con=engine,
            index=False,
            if_exists="append"
        )
        logger.info("%i records loaded" % rowcount)
        engine.dispose(close=True)
        return rowcount > 0
    except exc.SQLAlchemyError as error:
        logger.error("Error: %s" % error)
        return False

@op(ins={'start': In(None)},out=Out(bool))
def load_rent(start):
    logger = get_dagster_logger()
    rent = pd.read_csv("staging/rent.csv", sep="\t")
    try:
        engine = create_engine(postgres_connection_string,poolclass=NullPool)
        engine.execute("TRUNCATE rent;")
        rowcount = rent.to_sql(
            name="rent",
            schema="public",
            con=engine,
            index=False,
            if_exists="append"
        )
        logger.info("%i records loaded" % rowcount)
        engine.dispose(close=True)
        return rowcount > 0
    except exc.SQLAlchemyError as error:
        logger.error("Error: %s" % error)
        return False


@op(ins={'start': In(None)},out=Out(bool))
def load_homeless(start):
    logger = get_dagster_logger()
    homeless = pd.read_csv("staging/homeless.csv", sep="\t")
    try:
        engine = create_engine(postgres_connection_string,poolclass=NullPool)
        engine.execute("TRUNCATE homeless;")
        rowcount = homeless.to_sql(
            name="homeless",
            schema="public",
            con=engine,
            index=False,
            if_exists="append"
        )
        logger.info("%i records loaded" % rowcount)
        engine.dispose(close=True)
        return rowcount > 0
    except exc.SQLAlchemyError as error:
        logger.error("Error: %s" % error)
        return False
