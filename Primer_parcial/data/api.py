import pandas as pd
from sodapy import Socrata


def get_data(limite_registros, nombre_departamento):
    client = Socrata("www.datos.gov.co", None)
    results = client.get("gt2j-8ykr", limit=limite_registros, departamento_nom=nombre_departamento)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    return results_df
