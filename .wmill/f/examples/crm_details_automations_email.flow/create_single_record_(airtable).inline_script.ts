import * as wmill from "https://deno.land/x/windmill@v1.70.1/mod.ts";
import { Airtable } from "https://deno.land/x/airtable/mod.ts";

export async function main(at_con: wmill.Resource<"airtable">, at_table: wmill.Resource<"airtable_table">, first_name: string, last_name: string, email: string, company: string, role: string, what_company_does: string, automatic: boolean = true) {

    const airtable = new Airtable({...at_con, ...at_table});
    
    const new_record = {
        "First name": first_name,
        "Last name": last_name,
        "Email": email,
        "Company": company,
        "Role": role,
        "What company does": what_company_does,
        "Generated automatically": automatic
    };

    const createOne = await airtable.create(new_record);

    return { message: "Created record in table"}
}