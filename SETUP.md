# Firebase Setup Guide

This app requires a Firebase project for authentication and cloud storage.
Follow these steps once — it takes about 10 minutes.

---

## Step 1 — Create a Firebase Project

1. Go to [https://console.firebase.google.com](https://console.firebase.google.com)
2. Click **Add project** and follow the wizard (you can disable Google Analytics)
3. Once created, click **Continue**

---

## Step 2 — Enable Authentication

1. In the left sidebar, go to **Build → Authentication**
2. Click **Get started**
3. Under the **Sign-in method** tab, enable:
   - **Email/Password** — click it, toggle on, Save
   - **Google** — click it, toggle on, add a support email, Save

---

## Step 3 — Create Firestore Database

1. In the left sidebar, go to **Build → Firestore Database**
2. Click **Create database**
3. Choose **Start in production mode**, click Next
4. Pick a region (e.g. `europe-west1`), click **Enable**

---

## Step 4 — Set Firestore Security Rules

1. In Firestore, go to the **Rules** tab
2. Replace the existing rules with:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /classes/{classId} {
      allow read, update: if request.auth != null
        && request.auth.uid in resource.data.members;
      allow create: if request.auth != null;

      match /budgets/{budgetId} {
        allow read, write: if request.auth != null
          && request.auth.uid in get(/databases/$(database)/documents/classes/$(classId)).data.members;
      }
      match /gifts/{giftId} {
        allow read, write: if request.auth != null
          && request.auth.uid in get(/databases/$(database)/documents/classes/$(classId)).data.members;
      }
    }
  }
}
```

3. Click **Publish**

---

## Step 5 — Get Your App Config

1. In the left sidebar, click the gear icon next to **Project Overview** → **Project settings**
2. Scroll down to **Your apps** section
3. Click the **</>** (web) icon to add a web app
4. Give it a nickname (e.g. "vaad-app"), click **Register app**
5. Copy the `firebaseConfig` object shown

---

## Step 6 — Add Config to index.html

Open `index.html` and find this block near the top:

```js
const firebaseConfig = {
  apiKey:            "YOUR_API_KEY",
  authDomain:        "YOUR_PROJECT_ID.firebaseapp.com",
  projectId:         "YOUR_PROJECT_ID",
  storageBucket:     "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId:             "YOUR_APP_ID",
};
```

Replace each `"YOUR_..."` value with the corresponding value from your Firebase config.

---

## Step 7 — Deploy

Commit and push `index.html` to GitHub. GitHub Pages will automatically update your site at:

```
https://rottembz-prog.github.io/Vaad-app/
```

---

## How the app works after setup

- Each user signs in with their own account (Google or email)
- One parent **creates a group** and gets a 6-character **invite code**
- They share the code with other parents
- Other parents enter the code to **join the group**
- All group members share the same budgets and data in real time
