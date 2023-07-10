from pymongo import MongoClient
from dagster import op, Out, In, DagsterType
from dagster_pandas import PandasColumn, create_dagster_pandas_dataframe_type
from datetime import datetime
import pandas as pd

mongo_connection_string = "mongodb://dap:dap@127.0.0.1"

ImmigrationDataFrame = create_dagster_pandas_dataframe_type(
    name="ImmigrationDataFrame",
    columns=[
        PandasColumn.string_column("immigration_id",non_nullable=True, unique=True),
        PandasColumn.string_column("file_name", non_nullable=True),
        PandasColumn.string_column("year", non_nullable=True),
        PandasColumn.string_column("gender", non_nullable=True),
        PandasColumn.string_column("nationality", non_nullable=True),
        PandasColumn.string_column("unit", non_nullable=True),
        PandasColumn.string_column("value", non_nullable=True)
    ],
)

RentDataFrame = create_dagster_pandas_dataframe_type(
    name="RentDataFrame",
    columns=[
        PandasColumn.string_column("rent_id", non_nullable=True),
        PandasColumn.integer_column("year",  non_nullable=True),
        PandasColumn.string_column("number_of_bedrooms",  non_nullable=True),
        PandasColumn.string_column("property_type",non_nullable=True),
        PandasColumn.string_column("location",  non_nullable=True),
        PandasColumn.float_column("cost",  non_nullable=True)
    ],
)

HomelessDataFrame = create_dagster_pandas_dataframe_type(
    name="HomelessDataFrame",
    columns=[
        PandasColumn.string_column("homeless_id", non_nullable=True),
        PandasColumn.string_column("year",  non_nullable=True),
        PandasColumn.string_column("month",  non_nullable=True),
        PandasColumn.string_column("region",non_nullable=True),
        PandasColumn.string_column("total_adults",  non_nullable=True),
        PandasColumn.string_column("male_adults",  non_nullable=True),
        PandasColumn.string_column("female_adults",  non_nullable=True)
    ],
)


immigration_columns = {
    "_id": "immigration_id",
    "File Name": "file_name",
    "Year": "year",
    "Gender": "gender",
    "Nationality": "nationality",
    "Coin Unit": "unit",
    "Value": "value",

}

@op(ins={'start': In(bool)}, out=Out(ImmigrationDataFrame))
def extract_immigration(start) -> ImmigrationDataFrame:
    conn = MongoClient(mongo_connection_string)
    db = conn["housing"]
    immigration = pd.DataFrame(db.immigration.find({}))
    immigration.drop(
        columns=["File Label", "Year Clone", "Gender No", "Nationality Key"],
        axis=1,
        inplace=True
    )
    immigration.rename(
        columns=immigration_columns,
        inplace=True
    )
    conn.close()
    return immigration

@op(ins={'immigration': In(ImmigrationDataFrame)}, out=Out(None))
def stage_extracted_immigration(immigration):
    immigration.to_csv("staging/immigration.csv",index=False,sep="\t")

rent_columns = {
    "_id": "rent_id",
    "Year": "year",
    "Number of Bedrooms": "number_of_bedrooms",
    "Property Type": "property_type",
    "Location": "location",
    "Cost": "cost"
}

@op(ins={'start': In(bool)}, out=Out(RentDataFrame))
def extract_rent(start) -> RentDataFrame:
    conn = MongoClient(mongo_connection_string)
    db = conn["housing"]
    rent = pd.DataFrame(db.rent.find({}))
    rent.drop(
        columns=["Coin Unit"],
        axis=1,
        inplace=True
    )
    rent.rename(
        columns=rent_columns,
        inplace=True
    )
    conn.close()
    return rent

@op(ins={'rent': In(RentDataFrame)}, out=Out(None))
def stage_extracted_rent(rent):
    rent.to_csv("staging/rent.csv",index=False,sep="\t")

homeless_columns = {
    "_id": "homeless_id",
    "Year": "year",
    "Month": "month",
    "Region": "region",
    "Total Adults": "total_adults",
    "Male Adults": "male_adults",
    "Female Adults": "female_adults"
}

@op(ins={'start': In(bool)}, out=Out(HomelessDataFrame))
def extract_homeless(start) -> HomelessDataFrame:
    conn = MongoClient(mongo_connection_string)
    db = conn["housing"]
    homeless = pd.DataFrame(db.homeless.find({}))
    homeless.drop(
        columns=["Adults Aged 18-24", "Adults Aged 25-44", "Adults Aged 45-64", "Adults Aged 65+", "Number of people who accessed Private Emergency Accommodation", "Number of people who accessed Supported Temporary Accommodation",
                 "Number of people who accessed Temporary Emergency Accommodation", "Number of people who accessed Other Accommodation", "Number of Families",
                 "Number of Adults in Families", "Number of Dependants in Families"],
        axis=1,
        inplace=True
    )
    homeless.rename(
        columns=homeless_columns,
        inplace=True
    )
    conn.close()
    return homeless

@op(ins={'homeless': In(HomelessDataFrame)}, out=Out(None))
def stage_extracted_homeless(homeless):
    homeless.to_csv("staging/homeless.csv",index=False,sep="\t")








