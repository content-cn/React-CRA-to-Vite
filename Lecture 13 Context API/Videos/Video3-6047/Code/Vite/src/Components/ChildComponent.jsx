import GrandChildComponent from "./GrandChildComponent";
//Additional Task: Make use of context in the child component to provide the same color to the border 
import { useContext } from "react";
import { colorContext } from "../context";

const ChildComponent = () => {
  //Consuming color context
  const {color} = useContext(colorContext);
  return (
  <div
    style={{
      border: `10px solid`,
      // using color to style the border color
      borderColor: color,
      marginLeft: "50px",
      padding: "10px",
      fontSize: "30px",
      width: "300px"
    }}
  >
    <GrandChildComponent />
  </div>
)};

export default ChildComponent;
