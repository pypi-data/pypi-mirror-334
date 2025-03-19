import os
import argparse

import psycopg2
from tqdm import tqdm
from dotenv import load_dotenv

from relsyndgb.metadata import Metadata
from relsyndgb.data import load_tables, remove_sdv_columns


def legalize_table_name(table_name: str):
    # if table_name.upper() in ['GROUP']:
    #     return f'{table_name}_'
    return f'{table_name}'

# TABLE GENERATION FUNCTIONS
def get_foreign_key_reference(table_name, field, metadata):
    for relationship in metadata.relationships:
        if relationship['child_table_name'] == table_name and relationship['child_foreign_key'] == field:
            return relationship['parent_table_name'], relationship['parent_primary_key']
    return None, None

def create_table_query(table_name, metadata, varchar_length=255, pk_length=20):
    print("Creating table", table_name, "as", legalize_table_name(table_name))
    fields = metadata.tables[table_name].to_dict()['columns']
    fields_str = ''
    for field, values in fields.items():
        if values['sdtype'] == 'id':
            fields_str += f"{field} VARCHAR({pk_length})"
            # check if its the primary key
            table_meta = metadata.to_dict()['tables'][table_name]
            if 'primary_key' in table_meta and table_meta['primary_key'] == field:
                fields_str += ' PRIMARY KEY, '
            else: 
                parent, parent_field = get_foreign_key_reference(table_name, field, metadata)
                fields_str += f" REFERENCES {legalize_table_name(parent)}({parent_field}), "
            
        elif values['sdtype'] == 'categorical':
            fields_str += f"{field} VARCHAR({varchar_length}), "
        elif values['sdtype'] == 'numerical':
            fields_str += f"{field} FLOAT, "
        elif values['sdtype'] == 'boolean':
            fields_str += f"{field} BOOLEAN, "
        elif values['sdtype'] == 'datetime':
            fields_str += f"{field} DATE, "
        else:
            raise ValueError(f'Unknown type {values["type"]} for field {field}')
    fields_str = fields_str[:-2]
    query = f"CREATE TABLE IF NOT EXISTS {legalize_table_name(table_name)} ({fields_str});"
    return query


def execute_query(query, cursor, connection):
    try:
        # Execute the query
        cursor.execute(query)

        # Commit the transaction
        connection.commit()

    except psycopg2.Error as error:
        # Handle any errors that occur during query execution
        print("Error executing query:", error)


def execute_write_query(query, cursor, connection, values):
        try:
            # Execute the INSERT query with %s placeholder
            cursor.execute(query, values)
    
            # Commit the transaction
            connection.commit()
    
            #print("Query executed successfully")
    
        except psycopg2.Error as error:
            raise error
            # Handle any errors that occur during query execution
            # print("Error executing query:", error)


# psycopg2.extensions.register_adapter(float, lambda x: 'NULL' if pd.isna(x) else float(x))        
def insert_batch_rows(table_name, df, batch_size=100):
    insert_query = f"INSERT INTO {legalize_table_name(table_name)} VALUES (" + "%s,"*(len(df.columns)-1) + "%s)"
    rows = [tuple(row) for _, row in df.iterrows()]
    # Insert rows in batches
    total_rows = len(rows)
    batch_size = total_rows if batch_size > total_rows else batch_size
    for i in tqdm(range(0, total_rows, batch_size)):
        batch = rows[i:i+batch_size] if i+batch_size <= total_rows else rows[i:]
        cursor.executemany(insert_query, batch)
        connection.commit()
        # break


if __name__ == "__main__":
    load_dotenv()

    args = argparse.ArgumentParser()
    args.add_argument("--dataset-name", type=str, default="rossmann_subsampled")
    args.add_argument("--varchar-length", type=int, default=255)
    args.add_argument("--pk-length", type=int, default=25)
    args.add_argument("--drop", type=bool, default=True)
    args.add_argument("--partition", type=int, default=-1)
    args = args.parse_args()

    # Connect to the database
    print("Connecting to the PostgreSQL database...")
    connection = psycopg2.connect(host=os.environ.get('PG_HOST'),
                            port=os.environ.get('PG_PORT'),
                            user=os.environ.get('PG_USER'),
                            password=os.environ.get('PG_PASSWORD'),
                            # dbname=args.dataset_name.split("-")[0],
                            dbname="synthetic_data_dco0",
                            sslmode='require')

    cursor = connection.cursor()
    print("Connection successful")

    dataset_name = args.dataset_name
    print("Creating tables for", dataset_name)
    # CREATE TABLES
    # clear the database
    if args.drop:
        execute_query("DROP SCHEMA public CASCADE; CREATE SCHEMA public;", cursor, connection)

    # create the tables
    metadata = Metadata().load_from_json(f'/Users/martinjurkovic/Documents/github_projects/relsyndgb/data/downloads/{dataset_name}/metadata.json')
    tables = load_tables(f'/Users/martinjurkovic/Documents/github_projects/relsyndgb/data/downloads/{dataset_name}', metadata)
    tables, metadata = remove_sdv_columns(tables, metadata)
    table_names = list()
    # add parent tables first
    for relationship in metadata.relationships:
        table_names.append(relationship['parent_table_name'])
        
    for relationship in metadata.relationships:
        table_names.append(relationship['child_table_name'])

    table_names = list((dict.fromkeys(table_names)))
    for table_name in table_names:

        if args.partition <= 0:
            # drop the table if it exists
            query = f"DROP TABLE IF EXISTS {legalize_table_name(table_name)} CASCADE;"
            execute_query(query, cursor, connection)
        # create the table
        query = create_table_query(table_name, metadata, 
                                varchar_length=args.varchar_length, 
                                pk_length=args.pk_length)
        execute_query(query, cursor, connection)
        # insert the rows
        fields = metadata.to_dict()['tables'][table_name]['columns']
        # reorder the columns of tables to be like in the metadata
        table_data = tables[table_name][list(fields.keys())]
        # select the partition
        if args.partition > -1:
            p = args.partition
            table_data = table_data[100000 * p:100000 * (p+1)]
        # insert rows in batches
        insert_batch_rows(table_name, table_data, batch_size=10000)
