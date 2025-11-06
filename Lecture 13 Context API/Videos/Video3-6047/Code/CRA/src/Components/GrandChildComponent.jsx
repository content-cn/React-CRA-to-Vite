// importing the useContext hooks and color context
import { useContext } from "react";
import { colorContext } from "../context";

const GrandChildComponent = () => {

  //Consuming the context
  const {color} = useContext(colorContext)

  return (
  <p style={{ color: color }}>Color code: {color}</p>
)
};

export default GrandChildComponent;
