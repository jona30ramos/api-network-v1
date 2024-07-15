import psycopg2
import pandas as pd # type: ignore
from dotenv import load_dotenv # type: ignore
import os
load_dotenv()

params = {
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
}   
connection_string = "dbname='{database}' user='{username}' host='{host}' password='{password}' port={port}".format(**params)

def getDataFromDB(accountId):
    conecction = psycopg2.connect(connection_string)
    network_in = f'''
    SELECT * FROM prod_app.bi.network_analysis
    WHERE account_id IN (
        SELECT DISTINCT counterparty_account_id 
        FROM prod_app.bi.network_analysis
        WHERE account_id = {accountId}
    )
'''
    df_network = pd.read_sql_query(network_in, conecction)
    type_to_color_node = {
        'Comercio': '#ff914d',
        'Persona': '#091264'
    }

    status_to_color = {
        'Frozen&Locked': '#091264',
        'Active': '#009a34',
        'Frozen': '#39ABDC',
        'Locked': '#FFB500'
    }
    central_node_id = accountId  
    central_node_color = '#ff5757' 

    df_network['sources'] = df_network['sources'].astype(int)
    df_network['targets'] = df_network['targets'].astype(int)

    df_network['Node_Color_Sources'] = df_network['sources_type'].map(type_to_color_node)
    df_network['Node_Color_Target'] = df_network['target_type'].map(type_to_color_node)

    df_network['Outline_Node_Color_Sources'] = df_network['sources_status'].map(status_to_color)
    df_network['Outline_Node_Color_Target'] = df_network['target_status'].map(status_to_color)

    df_network.loc[df_network['sources'] == central_node_id, ['Node_Color_Sources']] = central_node_color
    df_network.loc[df_network['targets'] == central_node_id, ['Node_Color_Target']] = central_node_color

    df_network['sources'] = df_network['sources'].astype(str)
    df_network['targets'] = df_network['targets'].astype(str)

    conecction.close()
    return df_network.to_dict(orient='records')


