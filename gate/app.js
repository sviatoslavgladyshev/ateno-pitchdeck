// Shared sign-in code for the Ateno pitch deck pages (/en/, /ru/, /auth/, /admin/).
import { initializeApp } from "https://www.gstatic.com/firebasejs/{{SDK}}/firebase-app.js";
import { getAuth, sendSignInLinkToEmail, onAuthStateChanged, signOut }
  from "https://www.gstatic.com/firebasejs/{{SDK}}/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/{{SDK}}/firebase-firestore.js";

export const HOST = "{{HOST}}";
export const ADMIN = "{{ADMIN}}";
// One address for everything: sign-in is remembered per domain, so the .web.app copies send people to the real one.
if (/\.(web\.app|firebaseapp\.com)$/.test(location.hostname))
  location.replace(`https://${HOST}${location.pathname}${location.search}${location.hash}`);

export const app = initializeApp({{CONFIG}});
export const auth = getAuth(app);
export const db = getFirestore(app);
export const EMAIL_KEY = "ateno-pitch-email";
export const $ = id => document.getElementById(id);

export const NONCE_KEY = "ateno-pitch-nonce";

// Only invited addresses get a link. The page checks invited/<sha256(email)>: it can answer "is this one
// address invited?" but never lists anyone. (The rules check the real list again before showing the deck.)
export async function sha256(text) {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, "0")).join("");
}
export async function isInvited(email) {
  if (email === ADMIN) return true;
  const { doc, getDoc } = await import("https://www.gstatic.com/firebasejs/{{SDK}}/firebase-firestore.js");
  try { return (await getDoc(doc(db, "invited", await sha256(email)))).exists(); } catch { return false; }
}

export async function sendLink(email, lang) {
  auth.languageCode = lang;
  // A one-time key stays in this browser and rides in the link. /auth/ only signs in where the key matches,
  // so a forwarded email (opened anywhere else) does not work.
  const nonce = [...crypto.getRandomValues(new Uint8Array(16))].map(b => b.toString(16).padStart(2, "0")).join("");
  await sendSignInLinkToEmail(auth, email, {
    url: `https://${HOST}/auth/?next=${encodeURIComponent(location.pathname)}&n=${nonce}`, handleCodeInApp: true });
  localStorage.setItem(EMAIL_KEY, email);
  localStorage.setItem(NONCE_KEY, nonce);
}

export function currentUser() {
  return new Promise(res => { const off = onAuthStateChanged(auth, u => { off(); res(u); }); });
}

export const logout = () => signOut(auth);
