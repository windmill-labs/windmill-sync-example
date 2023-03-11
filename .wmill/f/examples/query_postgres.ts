import {  type Resource,  type Sql, pgSql } from "https://deno.land/x/windmill@v1.51.0/mod.ts";

export async function main(
  db: Resource<"postgresql"> = "$res:f/examples/demodb",
  query: Sql = "SELECT * FROM demo",
) {
  return (await pgSql(db)(query)).rows
}

