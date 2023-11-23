import boto3
import pymysql
from prettytable import PrettyTable
from IPython.display import display, HTML

# AWS credentials and region
aws_access_key = 'XXXXXXXXXXXXXXXXX'
aws_secret_key = 'XXXXXXXXXXXXXXXXX'
aws_region = 'us-east-1'

# Aurora DB cluster details
aurora_cluster_endpoint = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
aurora_db_name = 'empresas'
aurora_db_user = 'admin'
aurora_db_password = '123456789'

# Establishing AWS session
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

# Connect to the Aurora database
try:
    conn = pymysql.connect(
        host=aurora_cluster_endpoint,
        user=aurora_db_user,
        password=aurora_db_password,
        database=aurora_db_name,
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor
    )

    # Execute a sample SQL query
    with conn.cursor() as cursor:
        sql_query = "SELECT * FROM Empregado LIMIT 10;"
        cursor.execute(sql_query)
        results = cursor.fetchall()

        # Create a table and add rows
        table = PrettyTable()
        table.field_names = results[0].keys()
        for row in results:
            table.add_row(row.values())

        # Convert the table data to HTML
        html_code = table.get_html_string()
        with open('output.html', 'w') as f:
            f.write(html_code)

except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    conn.close()
