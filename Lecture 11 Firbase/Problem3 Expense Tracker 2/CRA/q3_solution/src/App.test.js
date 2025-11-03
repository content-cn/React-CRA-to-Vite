import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import user from "@testing-library/user-event";
import App from "./App";

import { getDocs } from "firebase/firestore";

jest.mock("firebase/firestore", () => {
  const mockGetDocs = jest.fn();
  const module = jest.requireActual("firebase/firestore");

  return {
    ...module,
    getDocs: mockGetDocs
  };
});

describe("App renders correctly", () => {
  test("App retrives expenses from firestore on mount", async () => {
    user.setup();
    getDocs.mockImplementation(() => {
      return {
        docs: [
          {
            id: "1",
            data: () => ({ text: "test expense", amount: "42" })
          }
        ]
      };
    });

    render(<App />);

    expect(getDocs).toHaveBeenCalled();
  });

  test("App renders expenses correctly", async () => {
    user.setup();
    getDocs.mockImplementation(() => {
      return {
        docs: [
          {
            id: "1",
            data: () => ({ text: "test expense", amount: "42" })
          }
        ]
      };
    });

    render(<App />);

    const expenseEl = await screen.findByRole("listitem");

    expect(expenseEl).toHaveTextContent("test expense");
    expect(expenseEl).toHaveTextContent("42");
  });
});
