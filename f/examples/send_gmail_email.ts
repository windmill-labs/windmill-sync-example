import * as wmill from "https://deno.land/x/windmill@v1.27.2/mod.ts";
import {
  encode as base64UrlEncode,
} from "https://deno.land/std@0.82.0/encoding/base64url.ts";

export async function main(
  gmail_auth: wmill.Resource<"gmail">,
  to_email: string,
  subject: string,
  message: string,
  userId: string = "me"
) {
  const token = gmail_auth["token"];

  const email_body = `From: <${userId}>\nTo: <${to_email}>\nSubject:\n\r\n\r${subject}\n${message}`;

  const email = base64UrlEncode(email_body);
  const SEND_EMAIL_URL =
    `https://gmail.googleapis.com/gmail/v1/users/${userId}/messages/send`;
  const body = {
    "raw": email,
  };
  const response = await fetch(SEND_EMAIL_URL, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      Authorization: "Bearer " + token,
    },
  });
  const response_json = await response.json();

  return response_json;
}