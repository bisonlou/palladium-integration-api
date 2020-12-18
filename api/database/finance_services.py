import os
import sys
import pyodbc
import subprocess

try:
    # s = subprocess.Popen('find / -name *odbc.so -type f', stdout=subprocess.PIPE, shell=True).communicate()
    # f, _ = s

    # You can change this particular loop to select whatever driver you prefer
    # print(f.decode().split())
    
    username = os.environ.get("USERNAME")
    server = os.environ.get("SERVER")
    database = os.environ.get("DATABASE")
    password = os.environ.get("PASSWORD")


    # conn =pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    conn =pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
except Exception:
    print(sys.exc_info())


def get_department_totals(donor, department, month, year):
    query = """
        SELECT
        ISNULL(SUM(dbo.Salary_Generation.Net_Amount),0),
        ISNULL(SUM(0.05 * dbo.Salary_Generation.Total_Earn_Amount),0),
        ISNULL(SUM(0.1 * dbo.Salary_Generation.Total_Earn_Amount),0),
        ISNULL(SUM(dbo.Salary_Generation.Goods_Amount),0),
        ISNULL(SUM(dbo.Salary_Generation.LST_Amount),0)
        FROM
        dbo.Branch_Master
        INNER JOIN
        dbo.Increment
        ON
        dbo.Branch_Master.Branch_ID = dbo.Increment.Branch_ID
        INNER JOIN
        dbo.Salary_Generation
        ON dbo.Increment.Increment_Id = dbo.Salary_Generation.Increment_ID
        INNER JOIN
        dbo.PRODUCT_MASTER
        ON
        dbo.Increment.Product_ID = dbo.PRODUCT_MASTER.Product_ID
        WHERE
        (dbo.Salary_Generation.Month = ?)
        AND (dbo.Salary_Generation.Year = ?)
        AND (dbo.PRODUCT_MASTER.Product_Name = ?)
        AND (dbo.Branch_Master.Branch_Name = ?)"""

    cursor.execute(query, (month, year, department, donor))
    return cursor.fetchall()


def get_gratuity_totals(month, year):
    query = """
        SELECT
        round(SUM(0.11 * dbo.GRATUITY.Basic),0)
        FROM
        dbo.GRATUITY WHERE (dbo.GRATUITY.Month = ?)
        AND (dbo.GRATUITY.Year = ?)
    """

    cursor.execute(query, (month, year))
    return cursor.fetchall()


def get_advace_totals(donor, department, month, year):
    query = """
       select Account,Loan_Amount from [Salary Advances] where
       Branch_Name = ?
       and Product_Name= ?
       and Month = ?
       and Year = ?
    """

    cursor.execute(query, (donor, department, month, year))
    return cursor.fetchall()


def get_transaction_years():
    query = "select To_Date FROM Company_Transaction"""
    cursor.execute(query)
    return cursor.fetchall()


def get_employees():
    query = "SELECT Emp_Name FROM Emp_Master WHERE Is_Left = 'N'"""
    cursor.execute(query)
    return cursor.fetchall()
