import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import user from "@testing-library/user-event";
import App from "./App";

import { onSnapshot } from "firebase/firestore";

vi.mock("firebase/firestore", async () => {
  const mockOnSnapshot = vi.fn();
  const module = await vi.importActual("firebase/firestore");

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