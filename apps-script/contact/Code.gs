/**
 * TG6-dev contact form backend (Google Apps Script).
 *
 * Receives a POST from contact.html, appends a row to the bound Google Sheet,
 * and emails you a notification. Free, no server required.
 *
 * Setup: see apps-script/README.md. The short version:
 *   1. Create a Google Sheet → Extensions → Apps Script.
 *   2. Paste this file in (replace the default Code.gs).
 *   3. Set NOTIFY_EMAIL below.
 *   4. Deploy → New deployment → Web app → Execute as: Me, Access: Anyone.
 *   5. Copy the /exec URL into ENDPOINT in contact.html.
 */

// ── Config ────────────────────────────────────────────────────────────
// Where submission notifications get emailed. Change to your real inbox.
var NOTIFY_EMAIL = 'dvelupr@proton.me';
// Tab name inside the spreadsheet. Created automatically if missing.
var SHEET_NAME = 'Leads';
// ──────────────────────────────────────────────────────────────────────

var HEADERS = ['Timestamp', 'Name', 'Email', 'Business', 'Service', 'Budget', 'Message'];

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};

    // Honeypot: bots fill the hidden "company_url" field. Drop silently.
    if (p.company_url) {
      return _json({ ok: true, skipped: 'spam' });
    }

    var name     = _clean(p.name);
    var email    = _clean(p.email);
    var business = _clean(p.business);
    var service  = _clean(p.service);
    var budget   = _clean(p.budget);
    var message  = _clean(p.message);

    if (!name || !email || !message) {
      return _json({ ok: false, error: 'Missing required fields' });
    }

    var sheet = _getSheet();
    var ts = new Date();
    sheet.appendRow([ts, name, email, business, service, budget, message]);

    _notify({ ts: ts, name: name, email: email, business: business,
              service: service, budget: budget, message: message });

    return _json({ ok: true });
  } catch (err) {
    return _json({ ok: false, error: String(err) });
  }
}

// Lets you open the /exec URL in a browser to confirm it's live.
function doGet() {
  return _json({ ok: true, service: 'TG6-dev contact endpoint' });
}

function _getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function _notify(d) {
  var subject = 'New lead: ' + d.name + (d.business ? ' (' + d.business + ')' : '');
  var lines = [
    'New contact form submission on TG6-dev.',
    '',
    'Name:     ' + d.name,
    'Email:    ' + d.email,
    'Business: ' + (d.business || '—'),
    'Service:  ' + (d.service || '—'),
    'Budget:   ' + (d.budget || '—'),
    '',
    'Message:',
    d.message,
    '',
    'Received: ' + d.ts,
  ];
  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    subject: subject,
    replyTo: d.email,         // hit reply to answer the lead directly
    body: lines.join('\n'),
  });
}

function _clean(v) {
  return (v == null ? '' : String(v)).trim();
}

function _json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
