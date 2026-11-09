// Shared code for the Ateno pitch deck pages (/en/, /ru/, /admin/).
// No emails are sent by the site. Access works with invitation links the admin creates and sends himself:
//   https://pitch.ateno.co/en/#i=<secret token>
// The visitor confirms the email the invitation was made for; the invitation then remembers this browser.
import { initializeApp } from "https://www.gstatic.com/firebasejs/{{SDK}}/firebase-app.js";
import { getAuth, signInAnonymously, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/{{SDK}}/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/{{SDK}}/firebase-firestore.js";

export const HOST = "{{HOST}}";
export const ADMIN = "{{ADMIN}}";
// One address for everything: the browser session is kept per domain.
if (/\.(web\.app|firebaseapp\.com)$/.test(location.hostname))
  location.replace(`https://${HOST}${location.pathname}${location.search}${location.hash}`);

export const app = initializeApp({{CONFIG}});
export const auth = getAuth(app);
export const db = getFirestore(app);
export const $ = id => document.getElementById(id);

export async function sha256(text) {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, "0")).join("");
}
export const randomToken = (n = 24) =>
  btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(n)))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");

// An invitation (or admin key) is stored under sha256(token + ":" + email): only someone with both can find it.
export const keyFor = (token, email) => sha256(`${token}:${email.trim().toLowerCase()}`);

// This browser's identity: an anonymous Firebase session that stays until the site data is cleared.
export function session() {
  return new Promise((res, rej) => {
    const off = onAuthStateChanged(auth, u => {
      if (u) { off(); res(u); }
      else signInAnonymously(auth).catch(e => { off(); rej(e); });
    });
  });
}

// "#i=abc&x=1" -> { i: "abc", x: "1" }
export const hashParams = () => new URLSearchParams(location.hash.replace(/^#/, ""));
