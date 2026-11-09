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

export async function sendLink(email, lang) {
  auth.languageCode = lang;
  // the link in the email opens /auth/, which signs in and comes back to this page
  await sendSignInLinkToEmail(auth, email, { url: `https://${HOST}/auth/?next=${encodeURIComponent(location.pathname)}`, handleCodeInApp: true });
  localStorage.setItem(EMAIL_KEY, email);
}

export function currentUser() {
  return new Promise(res => { const off = onAuthStateChanged(auth, u => { off(); res(u); }); });
}

export const logout = () => signOut(auth);
