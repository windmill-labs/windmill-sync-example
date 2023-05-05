import {
  pgSql,
  type Resource,
} from "https://deno.land/x/windmill@v1.34.0/mod.ts";

//PG parametrized statement. No SQL injection is possible.
export async function main(
  db: Resource<"postgresql"> = "$res:g/all/demodb",
  username: string,
) {
  const query = await pgSql(
    db,
  )`SELECT DISTINCT email
FROM users
WHERE username = ${username}`;
  return query.rows;
}