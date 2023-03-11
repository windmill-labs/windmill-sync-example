import psycopg

postgresql = dict


def main(
    pg_con: postgresql = "$res:f/examples/demodb", query: str = "SELECT * FROM demo"
):

    conn = psycopg.connect(**pg_con)
    cur = conn.cursor()
    cur.execute(f"{query};")
    if cur.description:
        res = cur.fetchall()
    else:
        res = None
    conn.commit()
    cur.close()
    conn.close()
    return res
