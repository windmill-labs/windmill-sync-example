import * as tesseract from "https://deno.land/x/tesseract@1.0.1/mod.ts";
import { writableStreamFromWriter } from "https://deno.land/std@0.145.0/streams/mod.ts";

export async function main(
  url: string = "https://i.stack.imgur.com/t3qWG.png",
) {
  const path = "tmpImage.png";

  const fileResponse = await fetch(url);

  if (fileResponse.body) {
    const file = await Deno.open(path, { write: true, create: true });
    const writableStream = writableStreamFromWriter(file);
    await fileResponse.body.pipeTo(writableStream);
  }
  const output = await tesseract.recognize(path);
  return { foo: output };
}
