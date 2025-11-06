import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";


const firebaseConfig = {
  apiKey: "Place your api key here",
  authDomain: "place your auth domain here",
  projectId: "place your project id here",
  storageBucket: "place your storage bucket here",
  messagingSenderId: "place your messaging sender id here",
  appId: "place your app id here",
  measurementId: "place your measurement id here"
};


const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };
