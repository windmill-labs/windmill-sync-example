// import { toWords } from "number-to-words@1"
import * as wmill from "windmill-client"

// fill the type, or use the +Resource type to get a type-safe reference to a resource
// type Postgresql = object
fooo
export async function main(
  a: number,
  b: "my" | "enum",
  //c: Postgresql,
  //d: wmill.S3Object, // for large files backed by S3 (https://www.windmill.dev/docs/core_concepts/persistent_storage/large_data_files)
  e = "inferred type string from default arg",
  f = { nested: "object" },
) {
  // let x = await wmill.getVariable('u/user/foo')
  return { foo: a };
}
