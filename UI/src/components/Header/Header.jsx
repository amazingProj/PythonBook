import "./Header.css";
import NavItem from "./NavItem/NavItem";

const Header = () => {
  return (
    <div className="header">
      <div className="headerLeft">
        <div className="headerInput">
          <input type="text" placeholder=" חפש בPythonBook " />
        </div>
      </div>

      <div className="headerCenter">
        <div className="headerOption headerOptionActive"></div>
        <div className="headerOption"></div>
        <div className="headerOption"></div>
        <div className="headerOption"></div>
        <div className="headerOption"></div>
      </div>

      <nav className="navbar">
        <ul className="navbar-nav"></ul>
      </nav>
    </div>
  );
};

export default Header;
