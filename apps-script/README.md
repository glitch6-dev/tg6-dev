# Application form backend

Google Apps Script that receives Tier 3 ("Get Launched") applications from
`apply.html`, appends them to an `Applications` tab in a Google Sheet, and
emails a notification to `dvelupr@proton.me`.

## Setup (5 steps)

1. Create a new Google Sheet (this is your private application log — its ID
   never goes in this repo).
2. In the Sheet: **Extensions -> Apps Script**. Delete the default code and
   paste in `Code.gs`.
3. **Deploy -> New deployment -> Web app.** Execute as: **Me**. Who has
   access: **Anyone**.
4. Authorize when prompted. Copy the **/exec** URL.
5. Paste that URL into the `ENDPOINT` constant in `../apply.html`.

Open the `/exec` URL in a browser — you should see
`{"ok":true,"service":"Zero to Shipping application endpoint"}`.

## Known limitation

Because `apply.html` posts with `mode: "no-cors"`, the browser receives an
opaque response and cannot read whether the Apps Script call actually
succeeded — so the form shows "thank you" even if the script erred (a crash,
hit quota, or a misconfigured deployment). If an application is missing from
the Sheet, check the Apps Script execution log directly (Apps Script editor →
Executions) and confirm the deployment is live.
