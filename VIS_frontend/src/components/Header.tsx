import {FC} from "react";
import {Button, Container, Nav, Navbar} from "react-bootstrap";
import {Link, useNavigate} from "react-router-dom";
import {useUserContext} from "../utils/providers/UserProvider.tsx";

export const Header:FC = () => {
    const {user} = useUserContext();
    const navigate = useNavigate();

    return (
        <Navbar expand="lg" className="bg-body-tertiary">
            <Container fluid>
                <Navbar.Brand href="/">VIS</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarScroll" />
                <Navbar.Collapse id="navbarScroll">
                    <Nav
                        className="me-auto my-2 my-lg-0"
                        style={{ maxHeight: '100px' }}
                        navbarScroll
                    >
                        <Nav.Link href="/">Domů</Nav.Link>
                        <Nav.Link href="/tests">Testy</Nav.Link>
                    </Nav>
                    <div className="d-flex">
                        {user ? (
                            <Button variant="outline-primary"><Link to="/profile" className="underline-none">Profil</Link></Button>
                        ) : (
                            <Button variant="outline-primary" onClick={() => navigate('/login')}>Přihlásit se</Button>
                        )}
                    </div>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}
