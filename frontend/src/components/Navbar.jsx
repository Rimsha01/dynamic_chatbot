import { Link } from 'react-router-dom';
import { FiMessageSquare, FiUpload, FiZap } from 'react-icons/fi';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        <FiZap size={24} />
        <span>Dynamic Chatbot</span>
      </div>
      <ul className="nav-links">
        <li>
          <Link to="/">
            <FiMessageSquare size={18} />
            Chat
          </Link>
        </li>
{/*         <li> */}
{/*           <Link to="/upload"> */}
{/*             <FiUpload size={18} /> */}
{/*             Upload */}
{/*           </Link> */}
{/*         </li> */}
      </ul>
    </nav>
  );
}

export default Navbar;