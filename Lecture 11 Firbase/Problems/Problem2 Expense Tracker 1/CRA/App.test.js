import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import user from "@testing-library/user-event";
import App from "./App";

import { addDoc, setDoc } from "firebase/firestore";

jest.mock("firebase/firestore", () => {
  const mockAddDoc = jest.fn();
  const mockSetDoc = jest.fn();

  const module = jest.requireActual("firebase/firestore");

  return {
    ...module,
    addDoc: mockAddDoc,
    setDoc: mockSetDoc
  };
});

describe("App renders correctly", () => {
  test("App adds expense to firestore when the form is submitted", async () => {
    user.setup();
    render(<App />);

    addDoc.mockImplementation(async () => {
      return { id: "1" };
    });

    const textInputEl = screen.getByPlaceholderText(/enter text/i);
    const amountInputEl = screen.getByPlaceholderText(/enter amount/i);
    const addBtnEl = screen.getByRole("button", { name: /add transaction/i });

    await user.type(textInputEl, "test text");
    await user.type(amountInputEl, "42");

    await user.click(addBtnEl);

    expect(addDoc).toHaveBeenCalled();
  });
  test("App updates the expense in firestore when the update form is submitted", async () => {
    user.setup();
    render(<App />);

    addDoc.mockImplementation(async () => {
      return { id: "1" };
    });

    setDoc.mockImplementation(async () => {
      return { id: "1" };
    });

    const textInputEl = screen.getByPlaceholderText(/enter text/i);
    const amountInputEl = screen.getByPlaceholderText(/enter amount/i);
    const addBtnEl = screen.getByRole("button", { name: /add transaction/i });

    await user.type(textInputEl, "test text");
    await user.type(amountInputEl, "42");

    await user.click(addBtnEl);

    const expenseItemEl = screen.getByRole("listitem");
    await user.hover(expenseItemEl);

    const editBtnEl = screen.getByAltText(/edit/i);
    await user.click(editBtnEl);

    const updateBtnEl = screen.getByRole("button", {
      name: /edit transaction/i
    });
    await user.click(updateBtnEl);

    expect(setDoc).toHaveBeenCalled();
  });
});
