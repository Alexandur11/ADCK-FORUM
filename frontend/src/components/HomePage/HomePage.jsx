import { useContext, useEffect } from "react";
import { Link } from "react-router-dom";
import AppContext from "../../context/AppContext";

const server = "http://127.0.0.1:8000";
const loginEndpoint = "login";
const loginUrl = `${server}/${loginEndpoint}/token`;
const token = JSON.parse(localStorage.getItem('token'))

export default function HomePage() {
  const context = useContext(AppContext);

  const logout = () => {
    localStorage.removeItem("token");
  };

  useEffect(() => {
  fetch(`${server}/categories`, {
    headers: {
      'Authorization': `bearer ${token}`
    }
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    return response.json();
  })
  .then((data) => console.log(data))
  .catch((error) => console.error('Error:', error));
}, []);

  return (
    <>
      {/* Navigation Bar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <a className="navbar-brand" href="#">
          Forum
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
            <Link to="categories" className="nav-link">
                Categories
            </Link>
            </li>
            {!context.token && (
              <li className="nav-item">
                <Link to="login" className="nav-link">
                  Login
                </Link>
              </li>
            )}
            {!context.token && (
              <li className="nav-item">
                <a className="nav-link" href="register_page.html">
                  Register
                </a>
              </li>
            )}
            <li className="nav-item">
              <a className="nav-link" href="admin_panel.html">
                Admin Panel
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="admin_panel.html">
                Owner Panel
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="messenger.html">
                Messenger
              </a>
            </li>
            {context.token && (
              <li className="nav-item">
                <Link to="login" className="nav-link" onClick={logout}>
                  Logout
                </Link>
              </li>
            )}
          </ul>
        </div>
      </nav>

      {/* Main Content Area */}
      <div className="container mt-4">
        <div className="row">
          <div className="col-lg-8">
            <h2>Forum Posts</h2>
            {/* Forum posts will go here */}
            <div className="card mb-3">
              <div className="card-body">
                <h5 className="card-title">Post Title</h5>
                <p className="card-text">Post content goes here...</p>
              </div>
              <div className="card-footer text-muted">
                Posted by Username on Date
              </div>
            </div>
            {/* Additional forum posts can be added similarly */}
          </div>

          {/* Sidebar */}
          <div className="col-lg-4">
            <h2>Forum Sidebar</h2>
            {/* Sidebar content goes here */}
            <div className="card mb-3">
              <div className="card-body">
                <h5 className="card-title">Sidebar Item</h5>
                <p className="card-text">Sidebar content goes here...</p>
              </div>
            </div>
            {/* Additional sidebar items can be added similarly */}
          </div>
        </div>
      </div>
    </>
  );
}
