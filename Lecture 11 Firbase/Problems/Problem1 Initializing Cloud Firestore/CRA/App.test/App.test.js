import "@testing-library/jest-dom";
import { db } from "./firebaseInit";

describe("Firebase is initialized correctly", () => {
  test("Firestore database object is exported correctly", () => {
    expect(db).toBeDefined();
  });
});
