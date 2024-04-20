import { Link } from "@remix-run/react";

const Navbar = () => {
    return (
        <nav style={{border: "1px solid black"}}>
            <ul style={{ listStyleType: "none", display: "flex", justifyContent: "space-around", padding: "0" }}>
                <li><Link to="/" style={{ textDecoration: "none", color: "black" }}>Home</Link></li>
                <li><Link to="/library" style={{ textDecoration: "none", color: "black" }}>Library</Link></li>
                <li><Link to="/player" style={{ textDecoration: "none", color: "black" }}>Player</Link></li>
                <li><Link to="/account" style={{ textDecoration: "none", color: "black" }}>Account</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
