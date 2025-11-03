import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import user from "@testing-library/user-event";
import App from "./App";

import { onSnapshot } from "firebase/firestore";

jest.mock("firebase/firestore", () => {
  const mockOnSnapshot = jest.fn();
  const module = jest.requireActual("firebase/firestore");

  return {
    ...module,
    onSnapshot: mockOnSnapshot
  };
});

describe("App renders correctly", () => {
  test("App retrives realtime expenses from firestore on mount", async () => {
    user.setup();
    render(<App />);

    expect(onSnapshot).toHaveBeenCalled();
  });
});
