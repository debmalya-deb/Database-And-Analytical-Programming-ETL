import webbrowser
from dagster import job
from extract import *
from transform import *
from load import *

@op(out=Out(bool))
def load_dimensions(immigrationdim, rentdim, homelessdim):
    return rentdim and homelessdim and immigrationdim

@job
def etl():
    load_dimensions(
        immigrationdim=load_immigration(
            stage_extracted_immigration(
                extract_immigration()
            )
        ),
        rentdim=load_rent(
            stage_extracted_rent(
                extract_rent()
            )
        ),
        homelessdim=load_homeless(
            stage_extracted_homeless(
                extract_homeless()
            )
        )
    )