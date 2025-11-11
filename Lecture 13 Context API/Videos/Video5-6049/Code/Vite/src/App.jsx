import './App.css';
import { useState } from 'react';
import Items from './components/Items.jsx';
import Navbar from './components/Navbar.jsx';


function App() {
  const [total, setTotal] = useState(0);
  const [item, setItem] = useState(0);
  return (
        <div className='App'>
          <h2>Shopping Cart</h2>
            <Navbar />
            <Items />
        </div>
  );
}
export default App;