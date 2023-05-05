// import * as wmill from "https://deno.land/x/windmill@v1.36.0/mod.ts"

export async function main(path: string) {
  Deno.writeTextFile(`./shared/${path}`, "foo");
}
