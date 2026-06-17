/**
 * Zero to Shipping — Tier 3 application backend (Google Apps Script).
 *
 * Receives a POST from apply.html, appends a row to the bound Google Sheet's
 * "Applications" tab, and emails a notification. No server required.
 *
 * Setup: see apps-script/README.md. Short version:
 *   1. Create a Google Sheet -> Extensions -> Apps Script.
 *   2. Paste this file in (replace the default Code.gs).
 *   3. Deploy -> New deployment -> Web app -> Execute as: Me, Access: Anyone.
 *   4. Copy the /exec URL into ENDPOINT in apply.html.
 */

// Where application notifications get emailed.
var NOTIFY_EMAIL = 'dvelupr@proton.me';
// Tab name inside the spreadsheet. Created automatically if missing.
var SHEET_NAME = 'Applications';

var HEADERS = ['Timestamp', 'Name', 'Email', 'Background', 'Goal',
               'Project', 'Timeline', 'Why'];

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};

    // Honeypot: bots fill the hidden "company_url" field. Drop silently.
    if (p.company_url) {
      return _json({ ok: true, skipped: 'spam' });
    }

    var row = {
      name:       _clean(p.name),
      email:      _clean(p.email),
      background: _clean(p.background),
      goal:       _clean(p.goal),
      project:    _clean(p.project),
      timeline:   _clean(p.timeline),
      why:        _clean(p.why)
    };

    if (!row.name || !row.email || !row.why) {
      return _json({ ok: false, error: 'Missing required fields' });
    }

    var sheet = _getSheet();
    var ts = new Date();
    sheet.appendRow([ts, row.name, row.email, row.background, row.goal,
                     row.project, row.timeline, row.why]);

    _notify(ts, row);
    return _json({ ok: true });
  } catch (err) {
    return _json({ ok: false, error: String(err) });
  }
}

// Lets you open the /exec URL in a browser to confirm it's live.
function doGet() {
  return _json({ ok: true, service: 'Zero to Shipping application endpoint' });
}

function _getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(HEADERS);
  }
  return sheet;
}

function _notify(ts, row) {
  var subject = 'New Get Launched application: ' + row.name;
  var body = [
    'Name: ' + row.name,
    'Email: ' + row.email,
    'Background: ' + row.background,
    'Goal: ' + row.goal,
    'Project: ' + row.project,
    'Timeline: ' + row.timeline,
    'Why: ' + row.why,
    '',
    'Received: ' + ts
  ].join('\n');
  MailApp.sendEmail(NOTIFY_EMAIL, subject, body);
}

function _clean(v) {
  return (v == null ? '' : String(v)).trim().slice(0, 2000);
}

function _json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
