import {
  pgSql,
  type Resource,
} from "https://deno.land/x/windmill@v1.34.0/mod.ts";

//PG parametrized statement. No SQL injection is possible.
export async function main(
  db: Resource<"postgresql"> = "$res:g/all/demodb",
  reason: string,
  username: string,
) {
  const query = await pgSql(
    db,
  )`UPDATE users
SET banned = true, ban_reason = ${reason}
WHERE username = ${username}`;
  return query.rows;
}
